from .typedef import UserData
from typing import List
from database import session
from models.model import UserModel


def getUsers() -> List[UserData]:
    try:
        users = session.query(UserModel).all()
        return users
    except Exception as e:
        raise FileNotFoundError(e)
    

def getUser(email: str) -> UserData:
    try:
       user = session.query(UserModel).filter(UserModel.email == email).first()
       if user:
           return user
    except FileNotFoundError as e:
        raise FileNotFoundError("User with given email doesn't exist!")
 


        