from fastapi import APIRouter, Depends

from app.models.user import User
from app.exceptions import APIError
from app.utils import authenticate_user_token

from app.schemas.status import StatusSchema
from app.schemas.friend import AddFriendForm, RemoveFriendForm

from app.repositories.user import UserRepository, get_user_repository
from app.repositories.friendship import FriendshipRepository, get_friendship_repository

router = APIRouter()


@router.post("/api/friends/add")
def add_friend_handler(
    form: AddFriendForm,
    user: User = Depends(authenticate_user_token),
    user_repository: UserRepository = Depends(get_user_repository),
    friendship_repository: FriendshipRepository = Depends(get_friendship_repository)
) -> StatusSchema:
    if form.target_login == user.login:
        return StatusSchema(status="ok")
    
    target_user = user_repository.find_by_login(form.target_login)
    if target_user is None:
        raise APIError(status_code=404, reason="Пользователь с указанным логином не найден.")

    elif friendship_repository.find_by_users(user_id=user.id, target_id=target_user.id):
        return StatusSchema(status="ok")
    
    friendship_repository.create(user_id=user.id, target_id=target_user.id)
    return StatusSchema(status="ok")


@router.post("/api/friends/remove")
def remove_friend_handler(
    form: RemoveFriendForm,
    user: User = Depends(authenticate_user_token),
    user_repository: UserRepository = Depends(get_user_repository),
    friendship_repository: FriendshipRepository = Depends(get_friendship_repository)
) -> StatusSchema:
    if form.target_login == user.login:
        return StatusSchema(status="ok")
    
    # TODO: 200 or 404 on undefined
    target_user = user_repository.find_by_login(form.target_login)
    if target_user is None:
        raise APIError(status_code=404, reason="Пользователь с указанным логином не найден.")
    
    friendship_repository.remove(user_id=user.id, target_id=target_user.id)
    return StatusSchema(status="ok")
