from sqlalchemy import Column , Integer , String , Boolean,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base ##reqiurement for sqlachemy model

#creating post table
class Post(Base):  #ORM data schema model
    """
    Responsible for defining the columns of our post table within postgres
    is used to query ,create,delete and update entries within the database.
    """
    __tablename__ = "posts"
    id = Column(Integer,primary_key=True,nullable=False)
    title =Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default="True",nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,
                        server_default=text('now()'))
    owner_id = Column(Integer , ForeignKey("users.id",ondelete="CASCADE"),
                      nullable=False) #we have to use data migration tool to change database on the go
    owner = relationship('User')

# creating User table
class User(Base):
    ##creating a user table in postgres
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,nullable=False)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,
                        server_default=text('now()'))
    phone_number = Column(String)

##creating votes tables
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),
                     primary_key=True)
    post_id = Column(Integer , ForeignKey("posts.id",ondelete="CASCADE"),
                     primary_key=True)

