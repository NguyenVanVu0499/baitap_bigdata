from bson.objectid import ObjectId
from fastapi import APIRouter, File, UploadFile
import os
import uuid
import shutil
import hashlib
import cv2
import time
from .src.lp_recognition import E2E
from .model import InsertSchema
from config.utils import (
    ResponseModel , 
    ResponseCreateModel, 
    ErrorResponseModel,
    )
router = APIRouter()
path = os.getcwd()
from database.mongo import database

from datetime import datetime

# datetime object containing current date and time



do_xe = database.get_collection("do_xe")
try:
    do_xe.create_index('ten_bien_so')
    do_xe.create_index('thoi_gian_vao')
    do_xe.create_index('thoi_gian_ra')
    do_xe.create_index('url_img')
    do_xe.create_index('trang_thai')
except Exception as error:
    print(error)

"""
chua vao lan nao
da vao dang o trong bai do
da vao nhung ko trong bai do 
"""

@router.post("/uploadfile/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    names = uploaded_file.filename.split(".")
    model = E2E()

    salt = uuid.uuid4().hex
    file_name = hashlib.sha256(salt.encode() + uploaded_file.filename.encode()).hexdigest()+ '.' + names[len(names)-1]
    file_location = "{0}/static/{1}".format(path, file_name)

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(uploaded_file.file, file_object)
    
    img = cv2.imread(r'{}'.format(file_location))
    model.predict(img)
    
    print(model.format())
    r = []

    if do_xe.count() == 0 :
        now = datetime.now()
        data = {
            'ten_bien_so': model.format(),
            'thoi_gian_vao': [now.strftime("%d/%m/%Y %H:%M:%S")],
            'thoi_gian_ra': [],
            'url_img': f'http://127.0.0.1:8081/static/{file_name}',
            'trang_thai': True
        }
        do_xe.insert_one(data)

    for i in do_xe.find({ 'ten_bien_so': model.format() }, { 'ten_bien_so': 1, 'trang_thai': 1 }):
        r.append(i)

    if len(r) == 0:
        now = datetime.now()
        data = {
            'ten_bien_so': model.format(),
            # 'thoi_gian_vao': [now.strftime("%d/%m/%Y %H:%M:%S")],
            'thoi_gian_vao': ["09/12/2021 08:00:27"],
            'thoi_gian_ra': [],
            'url_img': f'http://127.0.0.1:8081/static/{file_name}',
            'trang_thai': True
        }
        do_xe.insert_one(data)
        print("insert_one ")
    
    else:
        for i in do_xe.find({ 'ten_bien_so': model.format() }, { 'ten_bien_so': 1, 'trang_thai': 1 }):
            now = datetime.now()
            # print(now.strftime("%d/%m/%Y %H:%M:%S"))
            if i['trang_thai'] :
                data = {
                    'ten_bien_so': model.format() ,
                    'url_img': f'http://127.0.0.1:8081/static/{file_name}',
                    'trang_thai': False
                }
                do_xe.update({'_id': ObjectId(i['_id'])}, {'$set': data} )
                # do_xe.update({'_id': ObjectId(i['_id'])}, {'$push': { 'thoi_gian_ra': now.strftime("%d/%m/%Y %H:%M:%S") } })
                do_xe.update({'_id': ObjectId(i['_id'])}, {'$push': { 'thoi_gian_ra': "09/12/2021 18:00:27" } })
            else:
                data = {
                    'ten_bien_so': model.format() ,
                    'url_img': f'http://127.0.0.1:8081/static/{file_name}',
                    'trang_thai': True
                }
                do_xe.update({'_id': ObjectId(i['_id'])}, {'$set': data} )
                # do_xe.update({'_id': ObjectId(i['_id'])}, {'$push': { 'thoi_gian_vao': now.strftime("%d/%m/%Y %H:%M:%S") }})
                do_xe.update({'_id': ObjectId(i['_id'])}, {'$push': { 'thoi_gian_vao': "09/12/2021 08:00:27"}})
    
    return f'http://127.0.0.1:8081/static/{file_name}'



@router.get("/parking", summary="Get all parking info")
async def get_all_user_data(page_size:int = 10, page_num:int = 1):
    query = {}
    user_info = []
    # Calculate number of documents to skip
    skips = page_size * (page_num - 1)
    for n in do_xe.find(query).skip(skips).limit(page_size):
        n['_id'] = str(n['_id'])
        user_info.append(n)
    total_count = do_xe.count(query)

    user_data = {
        "users_info" : user_info,
        "total" : total_count
    }
    x = True if user_data else False
    return (lambda: ResponseModel(user_data,"Rỗng"), lambda: ResponseModel(user_data,"Lấy Ra Thành Công"))[x]()



