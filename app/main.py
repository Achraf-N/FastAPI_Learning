from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define the Post model
class Post(BaseModel):
    title: str
    content: str
    ispublished: bool = True  # Default value

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
    return {"data": my_posts}

# Create a new post
@app.post("/posts",status_code = status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    # Convert the Pydantic model to a dictionary
    post_dict = new_post.model_dump()
    
    #post_dict = new_post.dict()
    # Generate a new ID (simple increment for demonstration)
    post_dict["id"] = len(my_posts) + 1
    # Add the new post to the list
    my_posts.append(post_dict)
    return {"data": post_dict}



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
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} Not found')
    return {"data": post}


@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def get_posts(id: int):
    index = find_index_posts(id)
    if(index==-1):
        my_posts.pop(index)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} is Not found')
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_posts(id: int, post:Post):
    index = find_index_posts(id)
    if(index==-1):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} is Not found')
    post_dic = post.model_dump()
    post_dic['id'] = id
    my_posts[index] = post_dic
    return {"data":post_dic}