from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ProjectModel
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.repositories.crud import CrudRepository


class ProjectRepository(CrudRepository[ProjectModel, ProjectCreate, ProjectUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProjectModel, db)
