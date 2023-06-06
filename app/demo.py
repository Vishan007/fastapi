from fastapi import FastAPI ,Response , status , HTTPException,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas
from .database import engine , get_db
from typing import List
from .routers import user,post,auth

models.Base.metadata.create_all(bind=engine) ##this post will create table in database

app = FastAPI()


app.include_router(post.router)    #routing
app.include_router(user.router)    #routing
app.include_router(auth.router)    #routing

while True:

    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',
                                password='12345',cursor_factory=RealDictCursor) 

        cursor = conn.cursor()
        print("Database connection was sucessfull !")
        break
    except Exception as error:
        print("Connection to database failed")
        print("error",error)
        time.sleep(2)

@app.get("/")  ## path-"/"  
def root():
    return {"message": "This is my first API welcome!!!"}

#getting all the post with raw sql
@app.get("/posts",response_model=List[schemas.Post])   ##get is used to retrive data from server
def get_posts():
    cursor.execute("""SELECT * FROM posts""")  #regular sql
    posts = cursor.fetchall()      ##raw sql
    return posts

##creating the post with raw sql
@app.post("/posts" , status_code=status.HTTP_201_CREATED,response_model=schemas.Post)  #post is used to send data to server
def create_posts(post: schemas.PostCreate): ##extracting body from the payload
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
                   (post.title,post.content,post.published))  ##inserting new values to database
    new_post = cursor.fetchone()
    conn.commit()  ##to commit changes in database
    return new_post

##retriveing the single post with raw sql
@app.get("/posts/{id}",response_model=schemas.Post)  ##id is path parameter
def get_posts(id:int , response:Response):
    cursor.execute(""" SELECT * from posts where id = %s """,(str(id),))
    test_post = cursor.fetchone()
    if not test_post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"post with id :{id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id :{id} not found"}
    return test_post

##deleting a post with raw sql
@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id : int):
    #deleting a post
    #find the index in the array that has required ID
    cursor.execute(""" delete from posts where id = %s returning * """,(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id :{id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT) ##when deleting do not send any data   

##updating the particular post with raw sql
@app.put("/posts/{id}")
def update_post(id : int ,post: schemas.PostCreate):
    cursor.execute("""UPDATE posts SET title = %s,content=%s,published=%s WHERE id = %s RETURNING * """,
                   (post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id :{id} not found")
    
    return updated_post







