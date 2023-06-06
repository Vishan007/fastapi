from pydantic import BaseModel,EmailStr #data parsing and validation
from datetime import datetime
from typing import Optional
from pydantic.types import conint

"""
class Post(BaseModel):  #data schema by pydantic
    
    Schema/Pydantic models define the structure of a request and response.
    This ensure that when a user wants to create a post the request will only go through,
    if it has a structure we created like title and content in the body.
    
    title : str
    content : str
    published : bool = True #default value is true

"""
# creating Resquest Schemas
class PostBase(BaseModel):
    title : str
    content: str
    published: bool =True

    class Config:
        orm_mode = True

# Using Inheritance
class PostCreate(PostBase):
    pass

##user response schemas
class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True ##converting the sql alchemy model to pydantic model 

#creating Response Schemas
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner : UserOut

    class Config:
        orm_mode = True ##converting the sql alchemy model to pydantic model 

class PostOut(BaseModel):
    Post : Post
    votes : int

    class Config:
        orm_mode = True

##user request schemas
class UserCreate(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id : int
    dir : conint(ge=0,le=1)  #values 0 and 1 for like 1 and to remove like 0

