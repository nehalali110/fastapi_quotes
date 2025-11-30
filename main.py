from fastapi import FastAPI, Depends, HTTPException, status, Request
import Database.storage
from pydantic import BaseModel, Extra, Field
from datetime import datetime
from models.quote_models import GetQuery, PostQuery, PutQuery, user
import utils.helpers
import sqlite3



app = FastAPI()

@app.get('/')
@app.get('/home')
def home():
    return "Welcome to the Quotes Server"


@app.get('/quotes')
def get_quotes(request: Request, params: GetQuery = Depends()):
    with sqlite3.connect("Database/database.db") as con:
        cur = con.cursor()
        print(request.headers)
        token_data = utils.helpers.fetch_token_data(request.headers)

        # Terminate the process if error occurs
        if not token_data[0]: return token_data

        print(token_data)
        user_id = token_data[1]["user_id"]

        filtered_quotes = Database.storage.get_quotes_from_db(cur, user_id, params.author, params.search, params.limit)
        return filtered_quotes
        

@app.post("/quotes")
def post_quotes(request: Request, params: PostQuery):
    with sqlite3.connect("Database/database.db") as con:
        cur = con.cursor()
        token_data = utils.helpers.fetch_token_data(request.headers)

        # Terminate the process if error occurs
        if not token_data[0]: return token_data

        print(token_data)
        user_id = token_data[1]["user_id"]
        Database.storage.post_quotes_to_db(cur, user_id, params.text, params.author)
        return {"status": "success", "message": "created"}


@app.put("/quotes/{quote_id}")
def put_quotes(request: Request, quote_id: int, params: PutQuery):
    if params.text == None and params.author == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="text and author both cannot be empty")
    
    with sqlite3.connect("Database/database.db") as con:
        cur = con.cursor()
        token_data = utils.helpers.fetch_token_data(request.headers)

        # Terminate the process if error occurs
        if not token_data[0]: return token_data

        print(token_data)
        user_id = token_data[1]["user_id"]

        Database.storage.update_quotes_to_db(cur, user_id, quote_id, params.text, params.author)
        return {"status": "success", "message": "quote modified"}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")


@app.delete("/quotes/{quote_id}")
def delete_quotes(quote_id: int):
    with sqlite3.connect("Database/database.db") as con:
        cur = con.cursor()
        token_data = utils.helpers.fetch_token_data(request.headers)

        # Terminate the process if error occurs
        if not token_data[0]: return token_data

        print(token_data)
        user_id = token_data[1]["user_id"]
        Database.storage.delete_quotes_from_db(cur, user_id, quote_id)
        return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")

@app.post("/register")
def register_user(params: user, request: Request):
    with sqlite3.connect("Database/database.db") as con:
        cur = con.cursor()
        print(request.headers)
        Database.storage.create_user(cur, params.email, params.password)
        return {"msg": "success", "value": "created"}


@app.post("/login")
def login_user(params: user):
    with sqlite3.connect("Database/database.db") as con:
        cur = con.cursor()
        return Database.storage.verify_user(cur, params.email, params.password)

