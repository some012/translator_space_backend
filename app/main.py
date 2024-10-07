from fastapi import FastAPI

from app.config.settings.project import project_settings
from app.router import api_router

app = FastAPI(
    debug=True,
    title="Translator Space",
    version="v1",
)

app.include_router(api_router, prefix=project_settings.API_V1_STR)
