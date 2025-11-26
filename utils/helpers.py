from datetime import datetime
import Database.storage
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

def get_base_list(filtered_quotes, quotes):
    if filtered_quotes:
        return filtered_quotes
    return quotes

def add_timestamp():
    current_datetime = datetime.now()
    return current_datetime.strftime("%d-%m-%Y %H:%M:%S")

def generate_token(user_id, user_email):
    jwt_token_secret = os.getenv('JWT_SECRET')
    payload = {"user_id": user_id, "user_email": user_email}
    return jwt.encode(payload, jwt_token_secret, algorithm="HS256")