from pydantic import BaseModel, Field, ConfigDict, field_validator

from typing import Optional
from typing_extensions import Annotated

from app.schemas.country import CountryAlpha2

UserLogin = Annotated[str, Field(pattern=r"^[a-zA-Z0-9-]{1,30}$", description="Логин пользователя")]
UserEmail = Annotated[str, Field(min_length=1, max_length=50, description="E-mail пользователя")]
UserPassword = Annotated[str, Field(min_length=6, max_length=100)]  # TODO: validator
UserIsPublic = Annotated[bool, Field(description="Является ли данный профиль публичным")]
UserPhone = Annotated[str, Field(pattern=r"^\+[\d]{1,19}$", description="Номер телефона пользователя в формате +123456789")]
UserImage = Annotated[str, Field(min_length=1, max_length=200, description="Ссылка на фото для аватара пользователя")]


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    login: UserLogin
    email: UserEmail
    countryCode: CountryAlpha2 = Field(description="Код страны пользователя")
    isPublic: UserIsPublic
    phone: Optional[UserPhone] = Field(default=None)
    image: Optional[UserImage] = Field(default=None)


class ProfileForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    countryCode: Optional[CountryAlpha2] = Field(default=None)
    isPublic: Optional[UserIsPublic] = Field(default=None)
    phone: Optional[UserPhone] = Field(default=None)
    image: Optional[UserImage] = Field(default=None)


class RegisterForm(UserSchema):
    model_config = ConfigDict(extra="forbid", regex_engine="python-re")
    
    password: UserPassword = Field(description="Пароль пользователя")
    
    @field_validator("password")
    def check_password(cls, value):
        # convert the password to a string if it is not already
        value = str(value)
        # check that the password has at least 8 characters, one uppercase letter, one lowercase letter, and one digit
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")
        return value


class RegisterSchema(BaseModel):
    profile: UserSchema


class LoginForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    login: UserLogin = Field(description="Логин пользователя")
    password: UserPassword = Field(description="Пароль пользователя")


class LoginSchema(BaseModel):
    token: str = Field(description="Авторизационный токен")


class UpdatePasswordForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    oldPassword: UserPassword = Field(description="Старый пароль пользователя")
    newPassword: UserPassword = Field(description="Новый пароль пользователя")
