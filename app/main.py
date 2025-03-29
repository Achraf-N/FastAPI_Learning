from fastapi import FastAPI,Response,status,HTTPException,Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import List
from sqlalchemy.orm import Session
from app import models
from .database import engine,SessionLocal
from . import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Define the Post model
class Post(BaseModel):
    title: str
    content: str
    ispublished: bool = True  # Default value


while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastApi', user='postgres',password='00&Achraf&',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database was connected successfully')
        break
    except Exception as error:
        print("connection to database Faild")
        print('Error : ',error)
# Sample data
my_posts = [
    {"title": "title 1", "content": "content of books 1", "id": 1},
    {"title": "title 2", "content": "content of books 2", "id": 2},
]

# Root endpoint
@app.get("/sqlalchemy")
async def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/")
async def root():
    return {"data": my_posts}

# Get all posts
@app.get("/posts",response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return posts

# Create a new post
@app.post("/posts",status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post_created = models.Post(**new_post.dict())
    
    db.add(new_post_created)
    db.commit()

    db.refresh(new_post_created)
    return new_post_created



def find_posts(id):  #id: int is for validation
    for post in my_posts:
        if(post["id"] == id):
            return post
        

def find_index_posts(id):  #id: int is for validation
    for i,p in enumerate(my_posts):
        if(p["id"] == id):
            return i
    return -1


# Get last posts
@app.get("/posts/latest",response_model=schemas.Post)
async def get_latest():

    latest_post = my_posts[(len(my_posts)-1)]
    return latest_post


@app.get("/posts/{id}",response_model=schemas.Post)
async def get_posts(id: int,db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} Not found')
    return post


@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def get_posts(id: int,db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if(post_query.first()==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} is Not found')
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model=schemas.Post)
async def update_posts(id: int, post:Post,db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if(post_query.first()==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} is Not found')
    post_query.update(post.dict(),synchronize_session=False)

    db.commit()
    return post_query