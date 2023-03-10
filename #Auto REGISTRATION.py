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

@app.post("/Auto_rc_upload")
def Auto_rc_upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
