import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

SECRET = "my-secret"
ALGORITHM = "HS256"


class AccessToken(BaseModel):
    iss: str
    sub: int
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str


class JWTToken(BaseModel):
    access_token: str


def sign_jwt(user_id: int) -> JWTToken:
    now = time.time()
    payload = {
        "iss": "curso-fastapi.com.br",
        "sub": str(user_id),
        "aud": "curso-fastapi",
        "exp": now + (60 * 30),  # 30 minutes
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return JWTToken(access_token=token)


async def decode_jwt(token: str) -> AccessToken | None:
    try:
        decoded_token = jwt.decode(
            token, SECRET, audience="curso-fastapi", algorithms=[ALGORITHM]
        )
        access_token = AccessToken.model_validate(decoded_token)
        return access_token if access_token.exp >= time.time() else None
    except Exception as e:
        print(f"Error decoding JWT: {e}")
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> AccessToken:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        print(f"Authorization header: {authorization}")
        print(f"Scheme: {scheme}, Credentials: {credentials}")

        if not credentials or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code or scheme.",
            )

        payload = await decode_jwt(credentials)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token.",
            )
        return payload


async def get_current_user(
    token: Annotated[AccessToken, Depends(JWTBearer())],
) -> dict[str, int]:
    return {"user_id": token.sub}


def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return current_user
