from beanie import Document
from datetime import datetime,timezone
from pydantic import Field,field_validator
from typing import Optional
from bson import ObjectId


class LogBase(Document):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at:Optional[datetime]=None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by:Optional[str] = None
    is_deleted: bool = False




class BaseLogWithStatus(LogBase):
    is_active: bool = True
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None