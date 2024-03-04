from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing_extensions import Annotated
from typing import List
from datetime import datetime

from app.schemas.user import UserLogin


PostContent = Annotated[str, Field(max_length=1000, description="Текст публикации.")]
PostTag = Annotated[str, Field(max_length=20, description="Тэг публикации")]


class PostForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    content: PostContent
    tags: List[PostTag]


class PostSchema(PostForm):
    id: str
    content: PostContent
    author: UserLogin
    tags: List[PostTag]
    createdAt: datetime
    likesCount: int = 0
    dislikesCount: int = 0
    
    @field_validator("id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        return str(value)
    
