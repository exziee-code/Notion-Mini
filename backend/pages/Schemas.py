from pydantic import BaseModel, Field, ConfigDict
import uuid
from datetime import datetime

class PageCreate(BaseModel):
    title: str = Field(default="Untitled", max_length=200)
    content: str = ""

class PageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime