import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'user': os.getenv("MySQL_USERNAME"),
    'password': os.getenv("MySQL_PASSWORD"),
    'host': os.getenv("MySQL_HOST"),
    'database': os.getenv("MySQL_DATABASE")
}

AZURE_STORAGE_CONFIG = {
    'connection_string': os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
    'container_name': os.getenv("AZURE_STORAGE_CONTAINER_NAME")
}
