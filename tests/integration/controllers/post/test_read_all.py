import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from src.schemas.post import PostIn
    from src.services.post import PostService

    service = PostService()
    await service.create(
        PostIn(
            title="post 1",
            content="some content",
            published=True,
        )
    )
    await service.create(
        PostIn(
            title="post 2",
            content="some content",
            published=True,
        )
    )
    await service.create(
        PostIn(
            title="post 3",
            content="some content",
            published=False,
        )
    )


@pytest.mark.parametrize("published, total", [(True, 2), (False, 1)])
async def test_read_posts_by_status_success(
    client: AsyncClient, access_token: str, published: str, total: int
):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"published": published, "limit": 10}

    # When
    response = await client.get(
        "/posts", headers=headers, params=params, follow_redirects=True
    )

    # Then
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(content) == total


async def test_read_posts_limit_success(client: AsyncClient, access_token: str):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"published": True, "limit": 1}

    # When
    response = await client.get(
        "/posts", headers=headers, params=params, follow_redirects=True
    )

    # Then
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(content) == 1


async def test_read_posts_not_authenticated_fail(client: AsyncClient):
    # Given
    params = {"published": True, "limit": 1}

    # When
    response = await client.get(
        "/posts", params=params, headers={}, follow_redirects=True
    )

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_read_posts_empty_parameters_fail(client: AsyncClient, access_token: str):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.get(
        "/posts", headers=headers, params={}, follow_redirects=True
    )

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
