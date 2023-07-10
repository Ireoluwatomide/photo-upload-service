from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class PhotoUploadModel(BaseModel):
    id: int
    photo_name: str
    photo_url: str
    is_deleted: bool
    created_at: datetime
    deleted_at: Optional[datetime]
