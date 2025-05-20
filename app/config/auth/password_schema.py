from pydantic import BaseModel


class ResetPassword(BaseModel):
    new_password: str


class ChangePassword(ResetPassword):
    old_password: str
