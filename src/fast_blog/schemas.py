from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# shared fields go in the Base classes, then Create/Response add what's
# specific to input vs output. max lengths match the db columns so bad
# data gets rejected before it ever hits sqlalchemy
class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    # from_attributes lets pydantic read straight off the sqlalchemy
    # object instead of needing a dict
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_file: str | None
    # this one is the @property on the model, not an actual column
    image_path: str


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    user_id: int  # temp - should come from the logged in user once auth is added


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date_posted: datetime
    # nested so the client gets the author info without a 2nd request
    author: UserResponse
