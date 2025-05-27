from datetime import datetime

from pydantic import BaseModel


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    published_at: datetime | None
