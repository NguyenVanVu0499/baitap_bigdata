from fastapi import APIRouter, File, UploadFile
import os
import uuid
import shutil
import hashlib

router = APIRouter()
path = os.getcwd()

@router.post("/uploadfile/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    names = uploaded_file.filename.split(".")

    salt = uuid.uuid4().hex
    file_name = hashlib.sha256(salt.encode() + uploaded_file.filename.encode()).hexdigest()+ '.' + names[len(names)-1]
    file_location = "{0}/static/{1}".format(path, file_name)

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(uploaded_file.file, file_object)
        
    return f'http://127.0.0.1:8081/static/{file_name}'