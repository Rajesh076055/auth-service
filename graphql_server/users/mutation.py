from .typedef import UserData
import strawberry
import logging
from service.user.authService import registerUser


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def registerUser(name: str, email: str, 
                           number: int, password: str, 
                            address: str) -> UserData:
        try:
            user = registerUser(name, email, number, password, address)
            logging.debug("USER REGISTERED")
            return user
        except ValueError as ve:
            logging.error(f"ERROR USER REGISTRATION: {str(ve)}")
            raise ve
        except Exception as e:
            logging.error(f"ERROR USER REGISTRATION: {str(e)}")
            raise ValueError("Something wrong registering the user.")
    