from pydantic import AwareDatetime, BaseModel


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    published_at: AwareDatetime | None
