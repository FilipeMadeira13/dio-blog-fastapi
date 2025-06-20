from databases.interfaces import Record

from src.database import database
from src.exceptions import NotFoundPostError
from src.models.post import posts
from src.schemas.post import PostIn, PostUpdateIn


class PostService:
    async def read_all(
        self, limit: int, published: bool, skip: int = 0
    ) -> list[Record]:
        query = (
            posts.select()
            .where(posts.c.published == published)
            .limit(limit)
            .offset(skip)
        )
        return await database.fetch_all(query)

    async def read(self, post_id: int) -> Record:
        return await self.__get_by_id(post_id)

    async def create(self, post: PostIn) -> int:
        command = posts.insert().values(
            title=post.title,
            content=post.content,
            published=post.published,
            published_at=post.published_at,
        )
        return await database.execute(command)

    async def update(self, post: PostUpdateIn, post_id: int) -> Record:
        total = await self.count(post_id)
        if not total:
            raise NotFoundPostError

        data = post.model_dump(exclude_unset=True)
        command = posts.update().where(posts.c.id == post_id).values(**data)
        await database.execute(command)

        return await self.__get_by_id(post_id)

    async def delete(self, post_id: int) -> None:
        command = posts.delete().where(posts.c.id == post_id)
        await database.execute(command)

    async def count(self, post_id: int) -> int:
        query = "SELECT COUNT(id) AS total FROM posts WHERE id = :id"
        result = await database.fetch_one(query, {"id": post_id})
        return result.total

    async def __get_by_id(self, post_id: int):
        query = posts.select().where(posts.c.id == post_id)
        post = await database.fetch_one(query)
        if post is None:
            raise NotFoundPostError
        return post
