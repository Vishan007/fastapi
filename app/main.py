from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import user,post,auth,votes

# models.Base.metadata.create_all(bind=engine) ##this post will create table in database
# we are using alembic for data migration
app = FastAPI()

origins = ["*"] #list of domain names that can talk to our api

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)    #routing
app.include_router(user.router)    #routing
app.include_router(auth.router)    #routing
app.include_router(votes.router)

@app.get("/")  ## path-"/"  
def root():
    return {"message": "This is my first API welcome!!!"}