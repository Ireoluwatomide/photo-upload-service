import time
import psutil
import uvicorn
from typing import List
from utils.logging_util import logger
from fastapi import FastAPI, UploadFile
from models.photo_upload import PhotoUploadModel
from fastapi.middleware.cors import CORSMiddleware
from handlers.azure_handler import upload_file_to_azure
from handlers.database_handler import get_all_photos, add_photo_to_database


app = FastAPI(debug=True)

app.state.start_time = time.time()  # Store the start time in the app's state
app.state.requests_processed = 0

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)


@app.middleware("http")
async def count_requests(request, call_next):

    """
    Middleware to log and count each incoming HTTP request.

    This middleware function intercepts each incoming HTTP request. It logs the request's HTTP method,
    URL path, and status code, and increments the count of requests processed by the application.

    Args:
        request (Request): The incoming request.
        call_next (Callable): The next middleware or route in the ASGI app.

    Returns:
        Response: The response generated by the next middleware or route.
    """

    response = None
    try:
        response = await call_next(request)
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code}"
        )
    finally:
        app.state.requests_processed += 1
    return response


@app.get("/")
async def root():

    """
    Get the server status.

    This endpoint provides information about the server status, including the current server time,
    the server uptime, the number of requests processed by the server, and the current memory usage.

    Returns:
        dict: A dictionary with the following keys:
            - 'current_server_time': The current server time.
            - 'server_uptime': The time that the server has been running.
            - 'requests_processed': The number of requests that the server has processed.
            - 'memory_info': A dictionary with information about the current memory usage,
              including the total memory, available memory, percentage of memory used,
              used memory, and free memory.
    """

    # Get the current server time
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

    # Get the server uptime
    uptime_seconds = time.time() - app.state.start_time
    uptime = str(int(uptime_seconds // 3600)) + ":" + \
        str(int((uptime_seconds % 3600) // 60)) + \
        ":" + str(int(uptime_seconds % 60))

    # Get the current memory usage
    memory_info = psutil.virtual_memory()

    return {
        "current_server_time": current_time,
        "server_uptime": uptime,
        "requests_processed": app.state.requests_processed,
        "memory_info": {
            "total": memory_info.total,
            "available": memory_info.available,
            "percent": memory_info.percent,
            "used": memory_info.used,
            "free": memory_info.free
        }
    }


@app.get("/photos", response_model=List[PhotoUploadModel])
async def get_photos():

    """
    Endpoint to retrieve all photos from the database.

    Returns:
        List[PhotoModel]: List of PhotoModel instances representing photos.
    """

    return await get_all_photos()


@app.post("/photos", status_code=201)
async def add_photo(file: UploadFile):

    """
    Endpoint to upload a photo. The photo is stored in Azure Blob Storage and its 
    information is stored in the database.

    Args:
        file (UploadFile): File to upload

    Returns:
        dict: Status message
    """

    file_url = await upload_file_to_azure(file)
    await add_photo_to_database(file.filename, file_url)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=False)