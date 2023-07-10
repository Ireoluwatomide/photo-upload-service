import mysql.connector
from fastapi import HTTPException
from utils.logging_util import logger
from config.settings import DATABASE_CONFIG
from models.photo_upload import PhotoUploadModel


async def get_all_photos():

    """
    Retrieve all photos from the database.

    Returns:
        List[PhotoModel]: List of PhotoModel instances representing photos.

    Raises:
        HTTPException: If a database error occurs.
    """

    try:

        logger.info("Connecting to MySQL database to get all photos: %s",)

        cnx = mysql.connector.connect(**DATABASE_CONFIG)
        cur = cnx.cursor()
        cur.execute("SELECT * FROM photos_upload_service ORDER by id DESC")
        rows = cur.fetchall()

        logger.info("Retrieved all photos from MySQL database: %s",)

    except Exception as err:
        logger.error("Database connection error: %s", err)
        raise HTTPException(
            status_code=500, detail="Database connection error: {}".format(err))

    formatted_photos = [PhotoUploadModel(
        id=row[0],
        photo_name=row[1],
        photo_url=row[2],
        is_deleted=row[3],
        created_at=row[4],
        deleted_at=row[5]) for row in rows]

    cur.close()
    cnx.close()

    return formatted_photos


async def add_photo_to_database(filename: str, file_url: str):

    """
    Add a photo's information to the database.

    Args:
        filename (str): Name of the photo file.
        file_url (str): URL of the photo file in Azure Blob Storage.

    Raises:
        HTTPException: If a database error occurs.
    """

    try:

        logger.info(
            "Connecting to MySQL database to add a new photo to database: %s",)

        cnx = mysql.connector.connect(**DATABASE_CONFIG)
        cur = cnx.cursor()
        insert_query = ("INSERT INTO photos_upload_service (photo_name, photo_url, is_deleted) "
                        "VALUES (%s, %s, %s)")
        cur.execute(insert_query, (filename, file_url, False))
        cnx.commit()

        logger.info("Added a new photo to database: %s",)

    except Exception as err:
        logger.error("Database connection error: %s", err)
        raise HTTPException(
            status_code=500, detail="Database connection error: {}".format(err))

    cur.close()
    cnx.close()
