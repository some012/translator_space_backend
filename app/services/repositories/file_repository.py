from sqlalchemy.ext.asyncio import AsyncSession

from app.models import FileModel
from app.schemas.file import FileCreate, FileUpdate
from app.services.repositories.crud import CrudRepository


class FileRepository(CrudRepository[FileModel, FileCreate, FileUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(FileModel, db)
