from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings.project import project_settings
from app.enums.role import RoleTypes
from app.schemas.role import RoleCreate
from app.schemas.settings import SettingsCreate
from app.schemas.user import UserCreate
from app.services.role_service import RoleService
from app.services.settings_service import SettingsService
from app.services.user_service import UserService


async def init_db(db: AsyncSession) -> None:
    role_service = RoleService(db)
    user_service = UserService(db)
    settings_service = SettingsService(db)

    for name in RoleTypes:
        role = await role_service.get_by_name(name=name)
        if not role:
            role_in = RoleCreate(name=name)
            await role_service.create_role(role=role_in)

    print("role is created")

    superuser = await user_service.get_user_by_email(email=project_settings.SUPERUSER_LOGIN)

    if not superuser:
        superuser_in = UserCreate(
            name=project_settings.SUPERUSER_NAME,
            middle_name=project_settings.SUPERUSER_MIDDLE_NAME,
            last_name=project_settings.SUPERUSER_LAST_NAME,
            password=project_settings.SUPERUSER_PASSWORD,
            email=project_settings.SUPERUSER_LOGIN,
        )
        superuser = await user_service.create_user(user_in=superuser_in, user_role=RoleTypes.SUPERUSER)

        settings_in = SettingsCreate(user_sid=superuser.sid, activity=True)

        await settings_service.create_settings(settings=settings_in)

        print("settings is created")

    print("superuser is created")
