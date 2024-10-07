from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SettingsModel
from app.schemas.settings import SettingsCreate, SettingsUpdate
from app.services.repositories.crud import CrudRepository


class SettingsRepository(CrudRepository[SettingsModel, SettingsCreate, SettingsUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(SettingsModel, db)
