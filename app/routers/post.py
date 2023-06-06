from fastapi import Response, status , HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List , Optional
from ..database import get_db
from .. import models , schemas ,oauth2

router = APIRouter(
    prefix="/sqlalcposts" ,   ##helps to keep path name short
    tags=['Posts']
)

##SQL alchemy ORM functions to get all the posts
@router.get("/",response_model=List[schemas.PostOut]) ##get is used to retrive data from server
def get_posts(db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),
               limit :int = 10,skip:int=0,search:Optional[str]=""): #every time we work with database we have to pass this to interact with database
    
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  ## ORM for sql query
    
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,
                                         isouter=True).group_by(models.Post.id).filter(
                                            models.Post.title.contains(search)).limit(limit).offset(skip).all()
 
    return results

## ORM functions to create posts and save it in databse
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)): #this function forces user to login before creating a post
    #new_post = models.Post(title=post.title ,content = post.content,published=post.published) #creating new template for post
    new_post = models.Post(owner_id=current_user.id,**post.dict()) ##unpacking the dictonary
    db.add(new_post) ##adding to database
    db.commit() ##pushing into database  
    db.refresh(new_post) #retriving the post and storing it in new_post
    return new_post

##ORM functions to get the post by id
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int , db:Session=Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first() 
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,
                                         isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first() 
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"post with id :{id} not found")
    
    return post

##ORM functions to delete post by id
@router.delete("/{id}",status_code=status.HTTP_404_NOT_FOUND)
def delete_post(id:int , db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id :{id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT )

##ORM functions to Update post
@router.put("/{id}")
def update_post(id : int ,updated_post: schemas.PostCreate, db:Session=Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id :{id} not found")
    
    if post.owner_id != current_user.id: ##checking the post created user and deleting user are same
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()






