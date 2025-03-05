from sqlalchemy.orm import selectinload

from app.models import FileModel


class FileCustomOptions:
    @staticmethod
    def with_lines():
        return (selectinload(FileModel.lines),)
