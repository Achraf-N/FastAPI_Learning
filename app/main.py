from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

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
@app.get("/")
async def root():
    return {"data": my_posts}

# Get all posts
@app.get("/posts")
async def get_posts():
    cursor.execute("""Select * from posts """)
    posts = cursor.fetchall()
    return {"data": posts}

# Create a new post
@app.post("/posts",status_code = status.HTTP_201_CREATED)
async def create_post(new_post: Post):

    cursor.execute("""INSERT INTO posts (title,content,ispublished) VALUES (%s, %s, %s) RETURNING * """,(new_post.title,new_post.content,new_post.ispublished))
    new_post_created = cursor.fetchone()

    conn.commit()
    return {"data": new_post_created}



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
@app.get("/posts/latest")
async def get_latest():

    latest_post = my_posts[(len(my_posts)-1)]
    return {"data": latest_post}

# Get all posts
#Http status without build in function
"""
@app.get("/posts/{id}")
async def get_posts(id: int, response: Response):
    post = find_posts(id)
    if not post:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'message':f'post with id: {id} Not found'}
    return {"data": post}
"""

@app.get("/posts/{id}")
async def get_posts(id: int):
    cursor.execute("""Select * from posts where id=%s """,(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} Not found')
    return {"data": post}


@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def get_posts(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id),))
    delete_post = cursor.fetchone()

    conn.commit()
    if(delete_post==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} is Not found')
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_posts(id: int, post:Post):
    cursor.execute("""UPDATE posts SET title=%s, content = %s, ispublished = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.ispublished,str(id)))
    updating_post = cursor.fetchone()
    conn.commit()
    if(updating_post==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} is Not found')
    return {"data":updating_post}