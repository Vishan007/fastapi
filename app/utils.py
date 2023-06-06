from passlib.context import CryptContext 
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto") ##using bcrypt algorithm for hashing

def hash(password:str):   ###hashing the original password
    return pwd_context.hash(password)

def verify(plain_password,hashed_password):   ##checking the original password and provided password are equal
    return pwd_context.verify(plain_password,hashed_password)