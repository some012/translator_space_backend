from sqlalchemy.orm import selectinload

from app.models import UserModel


class UserCustomOptions:
    @staticmethod
    def with_role():
        return (selectinload(UserModel.role),)
