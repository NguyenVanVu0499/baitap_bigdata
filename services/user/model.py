from pydantic import BaseModel,EmailStr,Field, validator
from typing import Optional 
import re

class UserSchemaIn(BaseModel):
    ten_nguoi_dung :str = Field(...)
    mat_khau :str = Field(...)
    ten_day_du :str = Field(...)
    so_dien_thoai :str = Field(...)
    email :EmailStr = Field(...)
    anh_dai_dien :str = Field(...)    

    @validator('ten_nguoi_dung')
    def check_ten_nguoi_dung_match(cls, v):
        if ' ' in v or v is '':
            raise ValueError('Tên Đăng Nhập Không Hợp Lệ') 
        return v

    @validator('mat_khau')
    def check_mat_khau_match(cls, v):
        if ' ' in v or v is '':
            raise ValueError('Mật Khẩu Không Hợp Lệ') 
        return v
    
    @validator('so_dien_thoai')
    def check_so_dien_thoai(cls, v):
        matphone = re.search(re.compile("(?:84|03|05|07|08|09)([0-9]{8})$"), v)
        if not matphone :
            raise ValueError ("SDT Không Hợp Lệ , bắt đầu 03|05|07|08|09|84, có 10 số, Ví dụ: 0388888888")
        return v

    @validator('mat_khau')
    def check_mat_khau(cls, v):
        mat = re.search(re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"), v)
        if not mat:
            raise ValueError("Mật Khẩu Không Hợp Lệ ,Ví dụ: Hagiang@123")
        return v

    class Config:
        schema_extra={
            "example":
            {
                "ten_nguoi_dung" :"string",
                "mat_khau" :"B@ica0quen",
                "ten_day_du" : "",
                "so_dien_thoai" : "0388888888",
                "email" : "abc@gmail.com",
                "anh_dai_dien" : "",                
            }
        }


class UserSchemaOut(BaseModel):    
    ten_nguoi_dung :str = Field(...)
    ten_day_du :str = Field(...)
    so_dien_thoai :str = Field(...)
    email :EmailStr = Field(...)
    anh_dai_dien :str = Field(...)

    class Config:
        schema_extra={
            "example":
            {
                "ten_nguoi_dung" :"",
                "ten_day_du" : "",
                "so_dien_thoai" : "",
                "email" : "abc@gmail.com",
                "anh_dai_dien" : ""
            }
        }


class UpdateUserModel(BaseModel):
    ten_nguoi_dung :Optional[str]
    ten_day_du :Optional[str]
    so_dien_thoai :Optional[str]
    email :Optional[str]
    anh_dai_dien :Optional[str]
    ma_quyen_nguoi_dung :Optional[str]
    ten_quyen_nguoi_dung :Optional[str]
    # ten_chuc_vu :Optional[str]
    ma_chuc_vu :Optional[str]
    
    @validator('ten_nguoi_dung')
    def check_ten_nguoi_dung_match(cls, v):
        if ' ' in v or v is '':
            raise ValueError('Tên Đăng Nhập Không Hợp Lệ') 
        return v
    
    @validator('so_dien_thoai')
    def check_so_dien_thoai(cls, v):
        matphone = re.search(re.compile("(?:84|03|05|07|08|09)([0-9]{8})$"), v)
        if not matphone :
            raise ValueError ("SDT Không Hợp Lệ , bắt đầu 03|05|07|08|09|84, có 10 số, Ví dụ: 0388888888")
        return v


class UpdatePasswordModel(BaseModel):
    mat_khau :str = Field(...)
    
    class Config:
        schema_extra = {
            "example":
            {
                "password" :"",
            }
        }


class ChangePasswordSchema(BaseModel):
    mat_khau_cu: str = Field(...)
    mat_khau_moi: str = Field(...) 

    @validator('mat_khau_moi')
    def check_mat_khau_moi(cls, v):
        mat = re.search(re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"), v)
        if not mat:
            raise ValueError("Mật Khẩu Không Hợp Lệ ,Ví dụ: Hagiang@123")
        return v   
    
  