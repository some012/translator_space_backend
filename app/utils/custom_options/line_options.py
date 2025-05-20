from sqlalchemy.orm import selectinload

from app.models import LineModel


class LineCustomOptions:
    @staticmethod
    def with_file():
        return (selectinload(LineModel.file),)
