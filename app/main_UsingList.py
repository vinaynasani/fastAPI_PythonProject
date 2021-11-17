from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
import datetime
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

MY_POSTS = [{"title":"Some title1", "content": "Some Content1", "id":1},
            {"title":"Some title2", "content": "Some Content2", "id":2}
            ]

def get_post(id: int):
    for p in MY_POSTS:
        if p["id"] == id:
            return p

def get_index_of_post(id: int):
    for i, p in enumerate(MY_POSTS):
        if p['id'] == id:
            return i


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get('/')
def root():
    return {'message':'hello world'}

@app.get('/posts')
def get_posts():
    return {"data":MY_POSTS}

@app.get('/posts/{id}')
def get_single_post(id: int, response: Response):
    post = get_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail= f'Post with Id: {id} was not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"details": f'Post with Id: {id} was not found'}
    return post

@app.post('/posts', status_code = status.HTTP_201_CREATED)
def create_post(post: Post): # , response: Response
    post = post.dict()
    post["id"] = randrange(2,10000)
    MY_POSTS.append(post)
    #response.status_code = status.HTTP_201_CREATED
    return post
#title str, content str

@app.delete("/posts/{id}", status_code = status.HTTP_205_RESET_CONTENT)
def delete_post(id: int):
    index = get_index_of_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No post found for the ID: {id}")
    MY_POSTS.pop(index)
    return {"message":f"Post ID: {id} successfully deleted"}

@app.put('/posts/{id}', status_code = status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index = get_index_of_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No post found for the ID: {id}")
    new_post = post.dict()
    new_post['id'] = id
    MY_POSTS[index] = new_post
    return {"message":"Successfully updated Post", "details":new_post}
