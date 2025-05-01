from fastapi.security import OAuth2PasswordBearer

from app.config.settings import project_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=project_settings.API_V1_STR + "/auth/login", auto_error=False)
