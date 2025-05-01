import uvicorn

from app.config.settings import project_settings


def run():
    uvicorn.run(
        "app.main:app",
        host=project_settings.HOST,
        port=project_settings.PORT,
        reload=True,
        use_colors=True,
    )


if __name__ == "__main__":
    run()
