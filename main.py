from fastapi import FastAPI, Depends, HTTPException, status
import Database.storage
from pydantic import BaseModel, Extra, Field
from datetime import datetime
from models.quote_models import GetQuery, PostQuery, PutQuery
import utils.helpers

app = FastAPI()

@app.get('/')
@app.get('/home')
def home():
    return "Welcome to the Quotes Server"


@app.get('/quotes')
def get_quotes(params: GetQuery = Depends()):
    print(params)
    if params.author == None and params.search == None and params.limit == None:
        return quotes

    filtered_quotes = []
    while True:
        base_list = utils.helpers.get_base_list(filtered_quotes, quotes)
        if params.author:
            filtered_quotes = [quote for quote in base_list if quote['author'].lower() == params.author.lower().replace("+", "")]
            params.author = None
            continue
        elif params.search:
            filtered_quotes = [quote for quote in base_list if params.search.lower().replace("+", "") in quote['text'].lower()]
            params.search = None
            continue
        elif params.limit:
            filtered_quotes = base_list[:params.limit]
            params.limit = None
            continue
        else:
            return filtered_quotes
        

@app.post("/quotes")
def post_quotes(params: PostQuery):
    current_quote_id = quotes[-1].get('id', 0)
    new_quote = {'id': current_quote_id + 1, 
                 'text': params.text, 
                 'author': params.author,
                 'created_at': utils.helpers.add_timestamp()
                 }
    
    quotes.append(new_quote)
    return {"status": "success", "message": "created"}


@app.put("/quotes/{quote_id}")
def put_quotes(quote_id: int, params: PutQuery):
    if params.text == None and params.author == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="text and author both cannot be empty")
    
    for quote in quotes:
        if quote['id'] == quote_id:
            if params.text:
                quote['text'] = params.text
            elif params.author:
                quote['author'] = params.author
            else:
                quote['text'] = params.text
                quote['author'] = params.author
            
            quote['modified_at'] = utils.helpers.add_timestamp()
            return {"status": "success", "message": "quote modified"}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")


@app.delete("/quotes/{quote_id}")
def delete_quotes(quote_id: int):
    for quote in quotes:
        if quote['id'] == quote_id:
            quote['deleted_at'] = utils.helpers.add_timestamp()
            return {"status": "success", "detail": "quote deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")    
        

