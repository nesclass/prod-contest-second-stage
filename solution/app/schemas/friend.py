from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import UserLogin


class AddFriendForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    target_login: UserLogin = Field(alias="login")


class RemoveFriendForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    target_login: UserLogin = Field(alias="login")
