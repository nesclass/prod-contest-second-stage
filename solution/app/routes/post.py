from fastapi import APIRouter, Depends, Query

from app.models.user import User
from app.exceptions import APIError
from app.utils import authenticate_user_token

from app.repositories.user import UserRepository, get_user_repository
from app.repositories.post import PostRepository, get_post_repository
from app.repositories.friendship import FriendshipRepository, get_friendship_repository

from app.schemas.status import StatusSchema
from app.schemas.post import PostForm, PostSchema

router = APIRouter()


@router.post("/api/posts/new")
def post_publish_handler(
    form: PostForm,
    user: User = Depends(authenticate_user_token),
    post_repository: PostRepository = Depends(get_post_repository)
) -> PostSchema:
    post = post_repository.create(user=user, content=form.content, tags=form.tags)
    return PostSchema(
        content=post.content,
        tags=post.tags,
        id=post.id,
        author=post.user.login,
        createdAt=post.createdAt
    )


@router.get("/api/posts/{postId}")
def post_get_handler(
    postId: int,
    user: User = Depends(authenticate_user_token),
    post_repository: PostRepository = Depends(get_post_repository),
    friendship_repository: FriendshipRepository = Depends(get_friendship_repository)
) -> PostSchema:
    post = post_repository.find_by_id(post_id=postId)
    
    if post is None:
        raise APIError(status_code=404, reason="Указанный пост не найден.")
    
    elif user.id != post.user.id \
            and not post.user.isPublic \
            and friendship_repository.find_by_users(user_id=post.user.id, target_id=user.id) is None:
        raise APIError(status_code=404, reason="К указанному посту нету доступа.")
    
    return PostSchema(
        content=post.content,
        tags=post.tags,
        id=post.id,
        author=post.user.login,
        createdAt=post.createdAt
    )
