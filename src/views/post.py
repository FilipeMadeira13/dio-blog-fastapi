from pydantic import AwareDatetime, BaseModel, NaiveDatetime


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    published_at: AwareDatetime | NaiveDatetime | None
