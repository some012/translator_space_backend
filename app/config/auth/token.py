from typing import Annotated

from fastapi import HTTPException, Depends
from jwt import PyJWTError
from starlette import status

from app.config.auth.oauth2 import oauth2_scheme
from app.config.auth.token_helper import token_helper
from app.config.auth.token_schema import TokenData


def validate_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    incorrect_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин/пароль"
    )

    if not token:
        raise incorrect_credentials

    try:
        payload = token_helper.token_payload(token=token)
    except PyJWTError:
        raise incorrect_credentials
    except HTTPException:
        raise incorrect_credentials

    return payload
