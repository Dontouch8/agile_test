import sqlite3
from typing import Dict, Optional


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect("data.db")
    conn.row_factory = dict_factory

    return conn


def get_cursor(conn: sqlite3.Connection) -> sqlite3.Cursor:
    cursor = conn.cursor()
    return cursor


def create_images_table():
    conn = get_conn()
    cursor = conn.cursor()

    create_table = """
    CREATE TABLE IF NOT EXISTS images
        (
            image_id        TEXT PRIMARY KEY,
            author          TEXT,
            camera          TEXT,
            tags            TEXT,
            cropped_picture TEXT,
            full_picture    TEXT
        )
    """
    cursor.execute(create_table)
    conn.commit()
    conn.close()


def get_images_from_db(params: Dict[str, Optional[str]]) -> list:
    conn = get_conn()
    cursor = get_cursor(conn)
    for k in list(params.keys()):
        if params[k] is None:
            params.pop(k)
    if not params:
        return {"status": "error", "message": "No params was given"}
    where_query = ""
    for key in params.keys():
        where_query += f"{key}=? AND "
    where_query = where_query.rstrip("AND ")
    query = f"SELECT * FROM images WHERE {where_query}"
    cursor.execute(query, tuple(params.values()))
    return cursor.fetchall()
