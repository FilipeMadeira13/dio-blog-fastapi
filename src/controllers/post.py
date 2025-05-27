from fastapi import APIRouter, Depends, status
from src.database import database
from src.models.post import posts
from src.schemas.post import PostIn, PostUpdateIn
from src.security import login_required
from src.services.post import PostService
from src.views.post import PostOut

router = APIRouter(prefix="/posts", dependencies=[Depends(login_required)])
service = PostService()


@router.get("/", response_model=list[PostOut])
async def read_posts(limit: int, published: bool, skip: int = 0):
    return await service.read_all(limit=limit, published=published, skip=skip)


@router.get("/{post_id}", response_model=PostOut)
async def read_post(post_id: int):
    return await service.read_post(post_id=post_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(post: PostIn):
    return {**post.model_dump(), "id": await service.create_post(post=post)}


@router.patch("/{post_id}", response_model=PostOut)
async def update_post(post_id: int, post: PostUpdateIn):
    return await service.update_post(post=post, post_id=post_id)


@router.delete(
    "/{post_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_post(post_id: int):
    return await service.delete_post(post_id=post_id)
