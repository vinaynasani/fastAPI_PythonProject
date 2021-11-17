from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from sqlalchemy.engine import base
from starlette import status

from app.database import Base
from datetime import datetime

#pydantic model for Request or Response 
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config: # add it to make it pydantic model from orm model
        orm_mode = True


class UserLogin(BaseModel):
     email: EmailStr
     password: str


class PostBase(BaseModel):
    title: str
    published: bool = True
    content: str
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut #to return a related object and this class should be already defined in the above lines
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)