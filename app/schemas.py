from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
  title: str
  content: str
  ispublished: bool = True

class PostCreate(PostBase):
  pass


class Post(BaseModel):
  id: int
  title: str
  content: str
  ispublished: bool = True
  created_at: datetime
  class Config:
    orm_mode = True