from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from .authdb import authenticate_user, create_access_token,get_current_active_user
from .model import User,Token,TokenData
from bson.objectid import ObjectId

from database.mongo import database

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "05721706cc54c36f0e96ef655b542960757408b2761667be9319b78460184ddf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

router = APIRouter()

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data={
            "sub": user['ten_nguoi_dung'],
            "ten_day_du" :user["ten_day_du"],
            "so_dien_thoai": user["so_dien_thoai"],
            "email": user["email"],
            "anh_dai_dien": user["anh_dai_dien"],

        }  
    print(data)
    access_token = create_access_token(
        data=data, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, 'token_type': 'bearer','data':data}

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
