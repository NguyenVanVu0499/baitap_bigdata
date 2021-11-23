from fastapi import APIRouter, File, UploadFile
import os
import uuid
import shutil
import hashlib

router = APIRouter()
path = os.getcwd()

@router.post("/uploadfile/")
async def create_upload_file(upload_file: UploadFile = File(...)):
    names = upload_file.filename.split(".")
    