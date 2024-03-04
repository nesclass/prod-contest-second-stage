from fastapi import APIRouter, Depends, Query

from app.models.user import User
from app.exceptions import APIError
from app.utils import authenticate_user_token

from app.repositories.user import UserRepository, get_user_repository
from app.repositories.country import CountryRepository, get_country_repository
from app.repositories.friendship import FriendshipRepository, get_friendship_repository

from app.schemas.status import StatusSchema
from app.schemas.user import UserSchema, ProfileForm, UserLogin, UpdatePasswordForm

router = APIRouter()


@router.get("/api/me/profile", response_model_exclude_none=True)
def profile_get_handler(user: User = Depends(authenticate_user_token)) -> UserSchema:
    return UserSchema.model_validate(user)


@router.patch("/api/me/profile", response_model_exclude_none=True)
def profile_patch_handler(
    form: ProfileForm,
    user: User = Depends(authenticate_user_token),
    user_repository: UserRepository = Depends(get_user_repository),
    country_repository: CountryRepository = Depends(get_country_repository)
) -> UserSchema:
    if form.countryCode is not None and country_repository.find_country_by_alpha2(form.countryCode) is None:
        raise APIError(status_code=400, reason="Страны с указанным кодом не существует")

    user = user_repository.update_profile(
        login=user.login,
        countryCode=form.countryCode,
        isPublic=form.isPublic,
        phone=form.phone,
        image=form.image
    )

    return UserSchema.model_validate(user)


@router.get("/api/profile/{login}", response_model_exclude_none=True)
def find_profile_handler(
    target_login: UserLogin = Query(..., alias="login"),
    user: User = Depends(authenticate_user_token),
    user_repository: UserRepository = Depends(get_user_repository),
    friendship_repository: FriendshipRepository = Depends(get_friendship_repository)
) -> UserSchema:
    if user.login == target_login:
        return UserSchema.model_validate(user)
    
    target_user = user_repository.find_by_login(login=target_login)
    if target_user is None:
        raise APIError(status_code=403, reason="Профиль не может быть получен. Пользователь с указанным логином не существует.")
    
    if not target_user.isPublic and friendship_repository.find_by_users(user_id=target_user.id, target_id=user.id) is None:
        raise APIError(status_code=403, reason="Профиль не может быть получен. Нет доступа к запрашиваемому профилю.")
    
    return UserSchema.model_validate(target_user)


@router.post("/api/me/updatePassword")
def update_password_handler(
    form: UpdatePasswordForm,
    user: User = Depends(authenticate_user_token),
    user_repository: UserRepository = Depends(get_user_repository)
) -> StatusSchema:
    if form.oldPassword != form.newPassword:
        raise APIError(status_code=403, reason="Указанный пароль не совпадает с действительным.")
    user_repository.change_password(user.login, form.newPassword)
    return StatusSchema(status="ok")
