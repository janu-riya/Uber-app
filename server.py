from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from pymongo import MongoClient
import random, string

app = FastAPI()
client = MongoClient("mongodb://localhost:27017")
db = client["uber"]
#user

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
    
@app.delete("/user")
async def delete_user(email:str):
    try:
        filter = {
            'email' :email,

        }
        client.uber.user.delete_one(filter=filter)
        return True
    except Exception as e:
        print(str(e))
        return False


@app.post("/user")
async def create_user(user: User):
    try:
        client.uber.user.insert_one(dict(user))
        return True
    except Exception as e:
        print(str(e))
        return False
    
class CUser(BaseModel):
    query :dict ={}
    key: str
    value:str 

@app.put("/user")
async def change_user(user: CUser):
    try:
        filter= user.query
        update={
            '$set' :{
            user.key :user.value
            }
        }
        client.uber.user.update(filter,update=update)
        return True
    except Exception as e:
        print(str(e))
        return False

#Driver registration Model.....................................................

class Driver(BaseModel):
    name: str
    email: str
    license_no: str
    Aadhar_id: str
    password: str
    pan: str

@app.post("/driver")
async def create_driver(driver: Driver):
    try:
        filter ={
            'email': driver.email,
        }
        lfilter ={
            'license_no': driver.license_no,
        }
        afilter ={
            'Aadhar_id': driver.Aadhar_id,
        }
        pfilter ={
            'pan': driver.pan
        }
        if client.uber.driver.email == 0 and client.uber.driver.license_no == 0 and client.uber.driver.Aadhar_id == 0 and client.uber.driver.pan == 0:
            client.uber.driver.insert_one(dict(driver))
            return True
        else:
            return {"error":"not created"}
    except Exception as e:
        print(str(e))
        return False

@app.get("/driver")
async def get_driver(email:str):
    try:
        filter ={
        'email' : email,
        }
        project = {
        '_id':0,
        }
        client.uber.driver.find_one(filter=filter, project=project)
        return True
    except Exception as e:
        print(str(e))
        return False

class CDriver(BaseModel):
    query :dict ={}
    key: str
    value:str 

@app.put("/driver")
async def change_driver(driver: CDriver):
    try:
        filter= driver.query
        update={
            '$set' :{
            driver.key :driver.value
            }
        }
        client.uber.driver.update(filter,update=update)
        return True
    except Exception as e:
        print(str(e))
        return False

@app.delete("/driver")
async def delete_driver(email:str):
    try:
        filter = {
            'email' :email,

        }
        client.uber.driver.delete_one(filter=filter)
        return True
    except Exception as e:
        print(str(e))
        return False


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

#Creating trips model......................................................

class Trip(BaseModel):
    id : str =''.join(random.choices(string.ascii_letters + string.digits, k=16))
    starting_point: str
    ending_point: str
    distance: float
    customer_id: str
    driver_id: str
    fare:float = 50.0
    status: str = "Initiated"

@app.post("/trip")
async def create_trip(trip: Trip):
    try:
        filter={
            'email': trip.driver_id
        }
        ufilter={
            'email': trip.customer_id
        }
        if client.uber.trip.driver_id == 1 and client.uber.trip.customer_id == 1:
            client.uber.trip.insert_one(dict(trip))
            return trip.id
        else:
            return {"error":"not initiated"}
    
    except Exception as e:
        print(str(e))
        return False