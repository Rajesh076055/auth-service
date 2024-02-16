import os
import jwt
import logging
import secrets
import json
import hashlib
from database import session
from models.model import UserModel
from datetime import datetime, timedelta
from graphql_server.users.typedef import UserData
# from .emailService import send_verification_email


def commit_transaction():
    session.commit()


def rollback_transaction():
    session.rollback()


def user_verified(email: str) -> bool:
    user = session.query(UserModel).filter(UserModel.email == email).all()
    if user: return True
    else: return False


def generate_jwt_token(payload: str, expiration) -> str:
    try:
        payload_dict = json.loads(payload)
        payload_dict["exp"] = expiration
        jwt_token = jwt.encode(payload_dict, os.environ.get("JWT_SECRET"), algorithm='HS256')
        return jwt_token
    except (json.JSONDecodeError, jwt.PyJWTError) as e:
        print(f"Error generating JWT token: {e}")
        return None


async def validateToken(token: str) -> bool:
    try:
        payload = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms='HS256')
        if payload["exp"] > int(datetime.utcnow().timestamp()):
            return True
        return False
    
    except jwt.ExpiredSignatureError:
        return False
    
    except jwt.InvalidTokenError:
        return False


async def loginUser(email: str, password: str) -> str:
    try:
        user = session.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            logging.error("Attempt to login by non-existing user.")
            raise ValueError("User doesn't exists")

        hashed_password = hashlib.sha256(user.salt.encode() + password.encode()).hexdigest()
        if hashed_password == user.password:
            payload = {
                "user_id":user.id,
                "email":user.email
            }
            expiration_date = datetime.utcnow() + timedelta(hours=2)
            payload = json.dumps(payload)
            token = generate_jwt_token(payload, expiration_date)
            return token
        
        logging.error("Invalid password for user: %s", email)
        raise ValueError("Invalid password")

    except Exception as e:
        raise ValueError(e)


async def registerUser(name: str, email: str, number: int, password: str, address: str) -> UserData:
    try:
        existing_user = session.query(UserModel).filter(UserModel.email == email).first()

        if existing_user:
            logging.error("Duplicate User Error.")
            raise ValueError("User with the same email already exists")
    
        try:

            salt = secrets.token_bytes(8).hex()
            hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
        
        except Exception as e:
            logging.error("Hashing Error.")
            raise RuntimeError("An error occurred while hashing the password:", e)

        
        try:
            new_user = UserModel(
                name=name,
                email=email,
                number=number,
                password=hashed_password,
                salt=salt,
                address=address
            )
            
            session.add(new_user)
            session.commit()
            # verification_link = "http://localhost:5000/graphql"
            # send_verification_email(email, name, verification_link)

            # expiration_time = datetime.utcnow() + timedelta(minutes=2)
            
            # while datetime.utcnow() < expiration_time:
            # # Check if the user has verified within the timeframe
            #     if user_verified(email):
            #         commit_transaction()
            #         return new_user
            #     else:
            #         time.sleep(5)  # Sleep for 5 seconds before checking again

            # # If verification is not completed within the timeframe, rollback the changes
            # session.rollback()
            # raise RuntimeError("Email verification not completed within the specified timeframe.")


            
        except Exception as e:
            logging.error("User Creating Error.")
            rollback_transaction()
            raise RuntimeError("An error occured while creating the user.")
        
        return new_user

    except Exception as e:
        logging.error(f"Error during user registration: {e}")
        raise RuntimeError("An unexpected error occurred during user registration.")