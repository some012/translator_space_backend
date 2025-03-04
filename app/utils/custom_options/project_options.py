from sqlalchemy.orm import selectinload

from app.models import ProjectModel, FileModel


class ProjectCustomOptions:
    @staticmethod
    def with_files_and_lines():
        return (selectinload(ProjectModel.files).selectinload(FileModel.lines),)
