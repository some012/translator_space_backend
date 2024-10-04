from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LineModel
from app.schemas.line import LineCreate, LineUpdate
from app.services.repositories.crud import CrudRepository


class LineRepository(CrudRepository[LineModel, LineCreate, LineUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(LineModel, db)
