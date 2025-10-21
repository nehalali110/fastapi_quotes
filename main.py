from fastapi import FastAPI
from database.storage import quotes  

app = FastAPI()

@app.get('/')
@app.get('/home')
def home():
    return "Welcome to the Quotes Server"


@app.get('/quotes')
def get_quotes(author: str = None, search: str = None, limit: int = None):
    if author == None and search == None and limit == None:
        return quotes

    filtered_quotes = []
    while True:
        base_list = get_base_list(filtered_quotes, quotes)
        if author:
            filtered_quotes = [quote for quote in base_list if quote['author'].lower() == author.lower()]
            author = None
            continue
        elif search:
            filtered_quotes = [quote for quote in base_list if search.lower() in quote['text'].lower()]
            search = None
            continue
        elif limit:
            filtered_quotes = base_list[:limit]
            limit = None
            continue
        else:
            return filtered_quotes
        

def get_base_list(filtered_quotes, quotes):
    if filtered_quotes:
        return filtered_quotes
    return quotes