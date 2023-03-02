from fastapi import FastAPI

app = FastAPI()

@app.get("/user")
async def get_user(email: str):
    filter ={
        'email' : email,
    }

    try:
        client.uber.user.find_one(filter