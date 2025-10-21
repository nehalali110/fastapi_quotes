from fastapi import FastAPI 

app = FastAPI()

@app.get('/')
def welcome_home():
    return "Hey there what are you doing?"