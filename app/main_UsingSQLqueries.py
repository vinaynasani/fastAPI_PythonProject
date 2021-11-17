from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
import datetime
from pydantic import BaseModel, errors
from typing import Optional
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='FastApi',
                                user='postgres',
                                password='09241A0354v!nay',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection is successful")
        break
    except Exception as ex:
        print("connection to db failed")
        print("Error: ", ex)
        time.sleep(2)


@app.get('/')
def root():
    return {'message':'hello world'}

@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.get('/posts/{id}')
def get_single_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail= f'Post with Id: {id} was not found')
    return {"post_details":post}

@app.post('/posts', status_code = status.HTTP_201_CREATED)
def create_post(post: Post): # , response: Response
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    new_post = cursor.fetchone() # fetch one record to avoid brute force search
    conn.commit() # don't forget to commit the changes
    return {"data": new_post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No post found for the ID: {id}")
    return {"message":f"Post ID: {id} successfully deleted", "details":deleted_post}

@app.put('/posts/{id}', status_code = status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No post found for the ID: {id}")
    return {"message":"Successfully updated Post", "details":updated_post}
