from datetime import datetime
import Database.storage
import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timezone, timedelta
import jwt

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
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)
    payload = {"user_id": user_id, "user_email": user_email, "exp": expiry_time}
    return jwt.encode(payload, jwt_token_secret, algorithm="HS256")


def fetch_token_data(headers):
    try:
        token = headers.get('authorization').split(" ")[1]
        if not token:
            raise Exception("Unauthorized access")

        jwt_token_secret = os.getenv("JWT_SECRET")
        token_data = jwt.decode(token, jwt_token_secret, algorithms="HS256")
        return (1, token_data)    

    except AttributeError:
        return (0, {"error": "Invalid or empty token"})

    except Exception as e:
        return (0, {"error" : f"{e}"})







