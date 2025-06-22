from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controllers import auth, post
from src.database import database
from src.exceptions import NotFoundPostError


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


tags_metadata = [
    {
        "name": "auth",
        "description": "Operações para autenticação.",
    },
    {
        "name": "post",
        "description": "Operações para manter posts.",
        "externalDocs": {
            "description": "Documentação externa para Posts.api",
            "url": "https://post-api.com/",
        },
    },
]

servers = [
    {"url": "http://localhost:8000", "description": "Ambiente de desenvolvimento"},
    {
        "url": "https://dio-blog-fastapi-3jhy.onrender.com",
        "description": "Ambiente de produção",
    },
]


app = FastAPI(
    title="DIO Blog API",
    version="1.0.2",
    summary="API para blog pessoal",
    openapi_tags=tags_metadata,
    servers=servers,
    redoc_url=None,
    # openapi_url=None, # disable docs,
    lifespan=lifespan,
)
app.include_router(auth.router, tags=["auth"])
app.include_router(post.router, tags=["post"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NotFoundPostError)
async def not_found_post_exception_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Post not found!"},
    )
