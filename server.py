from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from pymongo import MongoClient
import random, string

app = FastAPI()
client = MongoClient("mongodb://localhost:27017")

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
        return dict(client.uber.user.find_one(filter=filter,projection=project))
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
    aadhar_id: str
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
            'Aadhar_id': driver.aadhar_id,
        }
        pfilter ={
            'pan': driver.pan
        }
        if client.uber.driver.count_documents(filter) == 0 and client.uber.driver.count_documents(lfilter) == 0 and client.uber.driver.count_documents(afilter) == 0 and client.uber.driver.count_documents(pfilter) == 0:
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
        return dict(client.uber.driver.find_one(filter=filter, projection=project))
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


@app.post("/driver_upload_files")
def driver_upload(file: UploadFile = File(...)):
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
    id : str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    starting_point:str
    ending_point:str
    distance:float
    customer_id:str
    driver_id:str
    vehicle_id:str
    fare:float = 50.0
    status: str = "initiated"
    


@app.get("/trip")
async def get_trip(id:str):
    try:
         filter ={
        'id' : id,
        }
         project = {
        '_id':0,
        }
         return dict(client.uber.trip.find_one(filter=filter,projection=project))
         
    except Exception as e:
        print(str(e))
        return False

@app.post("/trip")
async def create_trip(trip:Trip):
    
    try:
        filter={
        'email': trip.driver_id
        }
        ufilter = {
            "email": trip.customer_id
        }
        if(client.uber.driver.count_documents(filter)) == 1 and client.uber.user.count_documents(ufilter) == 1:
            client.uber.trip.insert_one(dict(trip))
            return trip.id
        else:
            return "not initiated"
            
    except Exception as e:
        print(str(e))
        return False
class CTrip(BaseModel):
    query :dict ={}
    key: str
    value:str 

@app.put("/trip")
async def change_trip(trip: CTrip):
    try:
        filter= trip.query
        update={
            '$set' :{
            trip.key :trip.value
            }
        }
        client.uber.trip.update(filter,update=update)
        return True
    
    except Exception as e:
        print(str(e))
        return False
    
@app.delete("/trip")
async def delete_trip(trip_id:str):
    try:
        filter = {
            'id' :id,

        }
        client.uber.trip.delete_one(filter=filter)
        return True
    except Exception as e:
        print(str(e))
        return False
    
#________________________________________________________CAR REGISTRATION________________________________________________________________

class Car(BaseModel):
    car_model : str
    registration_no : str
    insurance : str

@app.get("/car")
async def get_car(registration_no : str):
    try:
        filter ={
        
        'registration_no' : registration_no,
        
        }
        project = {
        '_id':0,
        }
        client.uber.car.find_one(filter=filter, project=project)
        return True
    except Exception as e:
        print(str(e))
        return False    

@app.post("/car")
async def create_car(car: Car):
    try:
        client.uber.car.insert_one(dict(car))
        return True
    except Exception as e:
        print(str(e))
        return False
    

class Ccar(BaseModel):
    query :dict ={}
    key: str
    value:str 

@app.put("/car")
async def change_car(car: Ccar):
    try:
        filter= car.query
        update={
            '$set' :{
            car.key :car.value
            }
        }
        client.uber.car.update(filter,update=update)
        return True
    except Exception as e:
        print(str(e))
        return False    

@app.delete("/car")
async def delete_car(registration_no:str):
    try:
        filter = {
            'registration_no' : registration_no,

        }
        client.uber.car.delete_one(filter=filter)
        return True
    except Exception as e:
        print(str(e))
        return False  

@app.post("/car_upload_files")
def car_upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}       
  
   #Bike REGISTRATION

class bike(BaseModel):
    bike_model : str
    bike_registration_number : str
    bike_insurance_number : str
    bike_number:str

@app.get("/bike")
async def get_bike(bike_registration_number : str):
    try:
        filter ={
        
        'bike_registration_number' : bike_registration_number,
        
        }
        project = {
        '_id':0,
        }
        client.uber.bike.find_one(filter=filter, project=project)
        return True
    except Exception as e:
        print(str(e))
        return False    

@app.post("/bike")
async def create_bike(bike: bike):
    try:
        client.uber.bike.insert_one(dict(bike))
        return True
    except Exception as e:
        print(str(e))
        return False
    

class Cbike(BaseModel):
    query :dict ={}
    key: str
    value:str 

@app.put("/bike")
async def change_bike(bike: Cbike):
    try:
        filter= bike.query
        update={
            '$set' :{
            bike.key :bike.value
            }
        }
        client.uber.bike.update(filter,update=update)
        return True
    except Exception as e:
        print(str(e))
        return False    

@app.delete("/bike")
async def delete_bike(bike_model:str):
    try:
        filter = {
            'bike_model' : bike_model,

        }
        client.uber.bike.delete_one(filter=filter)
        return True
    except Exception as e:
        print(str(e))
        return False 

@app.post("/bike_upload_files")
def bike_upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
 #Auto REGISTRATION

class Auto(BaseModel):
    Auto_model : str
    Auto_registration_number : str
    Auto_insurance_number : str
    Auto_number:str

@app.get("/Auto")
async def get_Auto(Auto_registration_number : str):
    try:
        filter ={
        
        'Auto_registration_number' : Auto_registration_number,
        
        }
        project = {
        '_id':0,
        }
        client.uber.Auto.find_one(filter=filter, project=project)
        return True
    except Exception as e:
        print(str(e))
        return False    

@app.post("/Auto")
async def create_Auto(Auto: Auto):
    try:
        client.uber.Auto.insert_one(dict(Auto))
        return True
    except Exception as e:
        print(str(e))
        return False
    

class CAuto(BaseModel):
    query :dict ={}
    key: str
    value:str 

@app.put("/Auto")
async def change_Auto(Auto: CAuto):
    try:
        filter= Auto.query
        update={
            '$set' :{
            Auto.key :Auto.value
            }
        }
        client.uber.Auto.update(filter,update=update)
        return True
    except Exception as e:
        print(str(e))
        return False    

@app.delete("/Auto")
async def delete_Auto(Auto_model:str):
    try:
        filter = {
            'Auto_model' : Auto_model,

        }
        client.uber.Auto.delete_one(filter=filter)
        return True
    except Exception as e:
        print(str(e))
        return False 

@app.post("/Auto_upload_files")
def Auto_upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
