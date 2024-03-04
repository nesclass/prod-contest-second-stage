from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from app.schemas.user import UserLogin


class FriendshipSchema(BaseModel):
    login: UserLogin
    added_at: datetime = Field(alias="addedAt")


class AddFriendForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    target_login: UserLogin = Field(alias="login")


class RemoveFriendForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    target_login: UserLogin = Field(alias="login")
