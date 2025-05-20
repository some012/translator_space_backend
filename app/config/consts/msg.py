from pydantic import BaseModel


class Msg(BaseModel):
    msg: str


class MsgLogin(Msg):
    agent: str
    platform: list
