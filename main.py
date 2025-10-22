from fastapi import FastAPI, Depends
from database.storage import quotes  
from pydantic import BaseModel, Extra

app = FastAPI()

@app.get('/')
@app.get('/home')
def home():
    return "Welcome to the Quotes Server"


class QuoteQuery(BaseModel, extra=Extra.forbid):
    author: str | None = None
    search: str | None = None
    limit: int | None = None

@app.get('/quotes')
def get_quotes(params: QuoteQuery = Depends()):
    print(params)
    if params.author == None and params.search == None and params.limit == None:
        return quotes

    filtered_quotes = []
    while True:
        base_list = get_base_list(filtered_quotes, quotes)
        if params.author:
            filtered_quotes = [quote for quote in base_list if quote['author'].lower() == params.author.lower()]
            params.author = None
            continue
        elif params.search:
            filtered_quotes = [quote for quote in base_list if params.search.lower() in quote['text'].lower()]
            params.search = None
            continue
        elif params.limit:
            filtered_quotes = base_list[:params.limit]
            params.limit = None
            continue
        else:
            return filtered_quotes
        

def get_base_list(filtered_quotes, quotes):
    if filtered_quotes:
        return filtered_quotes
    return quotes