from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel


class PostIn(BaseModel):
    title: str
    content: str
    published_at: datetime | None = None
    published: bool = False


class PostUpdateIn(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published_at: Optional[datetime] = None
    published: Optional[bool] = False
