from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.settings import project_settings
from app.router import api_router

app = FastAPI(
    debug=True,
    title="Translator Space",
    version="v1",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)
app.include_router(api_router, prefix=project_settings.API_V1_STR)
