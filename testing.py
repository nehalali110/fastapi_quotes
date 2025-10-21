from pydantic import BaseModel

class User(BaseModel):
    name : str
    age : int


user_input = User({"name": "adad", "age": 12})
print(user_input)

def introduce_user(user: User):
    print(f"Hey {user.name} how are you from {user.age} years?")

