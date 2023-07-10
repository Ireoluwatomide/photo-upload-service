from utils.logging_util import logger
from azure.core.exceptions import AzureError
from fastapi import HTTPException, UploadFile
from config.settings import AZURE_STORAGE_CONFIG
from azure.storage.blob import BlobServiceClient


async def upload_file_to_azure(file: UploadFile):

    """
    Upload a file to Azure Blob Storage.

    Args:
        file (UploadFile): File to upload

    Returns:
        str: URL of the uploaded file in Azure Blob Storage

    Raises:
        HTTPException: If an Azure Blob Storage error occurs.
    """

    try:
        logger.info("Connecting to Azure Blob storage: %s",)

        blob_service_client = BlobServiceClient.from_connection_string(
            AZURE_STORAGE_CONFIG['connection_string'])
        blob_client = blob_service_client.get_blob_client(
            AZURE_STORAGE_CONFIG['container_name'], file.filename)

        logger.info("Uploading file to Azure Blob storage: %s", file.filename)

        # # Stream file directly to blob storage
        # stream_uploader = blob_client.get_stream_uploader(overwrite=True)
        # async for chunk in file.iter_any(8192):
        #     stream_uploader.write(chunk)
        # stream_uploader.flush(close=True)

        # This reads the file into memory and then uploads it to blob storage
        # It is not recommended for large files
        data = await file.read()
        blob_client.upload_blob(data, overwrite=True)

        logger.info("File uploaded to Azure Blob storage: %s", file.filename)

        file_url = blob_client.url
    except AzureError as err:
        logger.error("Azure Blob storage error: %s", err)
        raise HTTPException(
            status_code=500, detail="Azure Blob storage error: {}".format(err))

    return file_url
