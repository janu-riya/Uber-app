from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

class User(BaseModel):
    name : str
    email : str
    password : str

@app.get("/user")
async def get_user(email: str):
    try:
        filter ={
        'email' : email,
        }
        project = {
        '_id':0,
        }
        client.uber.user.find_one(filter=filter, project=project)
        return True
    except Exception as e:
        print(str(e))
        return False
