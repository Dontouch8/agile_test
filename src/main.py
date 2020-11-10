from fastapi import FastAPI

from config import logger
from db import create_images_table, get_images_from_db

app = FastAPI()
create_images_table()


@app.get("/search/")
def get_images(
    image_id: str = None,
    author: str = None,
    camera: str = None,
    tags: str = None,
    cropped_picture: str = None,
    full_picture: str = None,
):

    params = {
        "image_id": image_id,
        "author": author,
        "camera": camera,
        "tags": tags,
        "cropped_picture": cropped_picture,
        "full_picture": full_picture,
    }
    logger.info(f"Received request with params: {params}")
    images = get_images_from_db(params)
    return images
