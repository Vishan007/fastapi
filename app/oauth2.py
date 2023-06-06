from jose import JWTError , jwt#token type
from datetime import datetime,timedelta
from fastapi import APIRouter ,Depends ,status ,HTTPException 
from fastapi.security import OAuth2PasswordBearer
from . import schemas , database ,models
import json
from sqlalchemy.orm import Session 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = 'wecanputanystringhere'   #secret key - dont store it in code
ALGORITHM = "HS256"   ##header algorithim 
ACCESS_TOKEN_EXPIRE_MINUTES = 60 #min expiration time for token

#signature = {header + payload + secret}  
#token = {header + signature + payload}

def serialize_datetime(obj):
    """
    the default argument of the json.dumps function to specify a 
    custom function that will be called to handle non-serializable objects.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def create_access_token(data:dict):   ##data dict is the payload
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id :str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Unable to validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token,credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
    




