from datetime import timedelta, datetime, timezone

import jwt
from fastapi import HTTPException
from starlette import status

from app.config.auth.token_schema import TokenData
from app.config.settings.project import project_settings


class TokenHelper:
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=project_settings.SECRET_KEY,
            algorithm=project_settings.ALGORITHM,
        )
        return encoded_jwt

    def token_payload(self, token: str) -> TokenData:
        payload = jwt.decode(
            token, project_settings.SECRET_KEY, algorithms=[project_settings.ALGORITHM]
        )

        email: str = payload.get("sub")

        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return TokenData(username=email)


token_helper = TokenHelper()
