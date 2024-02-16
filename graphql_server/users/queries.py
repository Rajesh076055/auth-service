from .typedef import UserData
from typing import List
import strawberry
from .resolvers import getUser, getUsers
from service.user.emailService import verifyEmail
from service.user.authService import loginUser, validateToken

@strawberry.type
class Query:
    getUsers: List[UserData] = strawberry.field(resolver=getUsers)
    getUser: UserData = strawberry.field(resolver=getUser)
    loginUser: str = strawberry.field(resolver=loginUser)
    validateToken: bool = strawberry.field(resolver=validateToken)
    verifyEmail: str = strawberry.field(resolver=verifyEmail)
