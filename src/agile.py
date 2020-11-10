import json
import sqlite3

import requests

from config import logger
from db import create_images_table, get_conn, get_cursor

API_KEY = "23567b218376f79d9415"
API_URL = "http://interview.agileengine.com"
HEADERS = {"Content-Type": "application/json", "user-agent": "PostmanRuntime/7.26.8"}


def request(page: int, token: int) -> dict:
    """
    Request to get list of images from
     /images endpoint with pagination.
    """
    logger.info(f"Sending request to page {page}")
    response = requests.get(
        f"{API_URL}/images",
        params={"page": str(page)},
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code != 200:
        error = f"Couldn't get images, {response.status_code}"
        return {"status": "error", "message": error}
    data = json.loads(response.text)
    return data


def get_token() -> dict:
    """
    Get Authorization token from /auth endpoint.
    """

    logger.info("Sending token request")
    payload = {"apiKey": API_KEY}
    response = requests.post(
        f"{API_URL}/auth", headers=HEADERS, data=json.dumps(payload)
    )
    if response.status_code == 200:
        token = json.loads(response.text).get("token")
    else:
        error = f"Couldn't get token, {response.status_code}"
        return {"status": "error", "message": error, "data": None}
    return {"status": "success", "message": None, "data": token}


def get_images():
    """
    Get all images from /images endpoint
    and add it to db.
    """

    conn = get_conn()
    cursor = get_cursor(conn)
    token = get_token()
    if token.get("status") == "error":
        return {"status": "error", "message": token.get("message")}
    page = 1
    first_page_response = request(page, token["data"])
    if first_page_response.get("status") == "error":
        return {"status": "error", "message": first_page_response.get("message")}
    results = []
    results.extend(first_page_response["pictures"])
    total_pages = first_page_response["pageCount"]
    while page < total_pages:
        response = request(page + 1, token["data"])
        if response.get("status") == "error":
            return {"status": "error", "message": response.get("message")}
        results.extend(response["pictures"])
        page += 1
    for i, image in enumerate(results, start=1):
        if i % 10 == 0:
            logger.info(f"Getting details for image {i}/{len(results)}")
        item = get_image_info(image["id"], token["data"])
        add_to_db(item, conn, cursor)
    conn.close()
    logger.info("Received all images")
    return {"status": "success"}


def get_image_info(id: str, token: str) -> dict:
    """
    Get more photo details.
    """

    response = requests.get(
        f"{API_URL}/images/{id}", headers={"Authorization": f"Bearer {token}"}
    )
    data = json.loads(response.text)
    return data


def add_to_db(item: dict, conn: sqlite3.Connection, cursor: sqlite3.Cursor):
    """
    Add photo detains to db.
    """

    query = "INSERT INTO images VALUES (?,?,?,?,?,?)"
    try:
        cursor.execute(
            query,
            (
                item["id"],
                item.get("author"),
                item.get("camera"),
                item.get("tags"),
                item.get("cropped_picture"),
                item.get("full_picture"),
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
