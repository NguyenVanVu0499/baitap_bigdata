
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from .model import UserSchemaIn, UpdateUserModel, ChangePasswordSchema
import re
from services.auth.authdb import get_current_active_user
# from passlib.context import CryptContext
from database.mongo import database


from config.utils import (
    ResponseModel , 
    ResponseCreateModel, 
    ErrorResponseModel,
    )
    
from .userdb import (
    create_user,
    get_all_user,
    update_user,
    delete_user,
    change_password,    
)

router = APIRouter()
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# def get_password_hash(password):
#     return pwd_context.hash(password)

@router.get("/user", summary="Get all user")
async def get_all_user_data(current_user = Depends(get_current_active_user), user_name:str= None,page_size:int = 10, page_num:int = 1):
    user_infos = await get_all_user(current_user, user_name=user_name, page_size=page_size, page_num=page_num)
    x = True if user_infos else False
    return (lambda: ResponseModel(user_infos,"Rỗng"), lambda: ResponseModel(user_infos,"Lấy Ra Thành Công"))[x]()


@router.post("/user", summary="Create New User")
# async def insert_user(current_user = Depends(get_current_active_user),  user_input:UserSchemaIn=Body(...)):
async def insert_user(user_input:UserSchemaIn=Body(...)):
    user = jsonable_encoder(user_input)

    # new_user = await create_user(user, current_user)
    new_user = await create_user(user)
    if new_user == 2:
        return ErrorResponseModel(f"{user['ten_nguoi_dung']} Đã Tồn Tại" , 422 ," Lỗi !")
    elif new_user == 4:
        return ErrorResponseModel(f" {user['ma_quyen_nguoi_dung']} Không Tồn Tại" , 422 ," Lỗi !")
    elif new_user == 3:
        return ResponseCreateModel("Tạo Thành Công")
    else:
        return ErrorResponseModel(f"Lỗi" , 400 ," Lỗi !")



@router.put("/user/{user_id}", summary= "Update User")
async def update_user_data(user_id: str, current_user = Depends(get_current_active_user), req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    
    updated_user = await update_user(user_id, req)
    
    if updated_user == 2:
        return ErrorResponseModel(f"{req['ten_nguoi_dung']} Đã Tồn Tại" , 409 ,"Tên Tài Khoản Đã Tồn Tại")
    if updated_user == 3:
        return ResponseModel(
            "Cập Nhật Thành Công!","OK"
        )
    else:
        return ErrorResponseModel(
            "Đã Có Lỗi Xảy Ra",
            404,
            "Lỗi Cập Nhật Tài Khoản.",
        )


@router.delete("/user/{user_id}",summary = "Delete a user, Update status user")
async def delete_user_data(user_id:str, force:bool, current_user = Depends(get_current_active_user)):
    deleted_user = await delete_user(user_id, force=force)
    x = True if deleted_user else False
    return (lambda: ErrorResponseModel("Lỗi",404,f"không tồn tại"), lambda: (lambda: ResponseModel(f"Ok","Thay Đổi Thành Công"), lambda: ResponseModel(f"Ok","Xoá Thành Công"))[force]())[x]()


# @router.put("/", summary= "Change password")
# async def change_password_user(user = Depends(get_current_active_user), req: ChangePasswordSchema = Body(...)):    
#     req = {k: v for k, v in req.dict().items() if v is not None}  
     
#     updated_password = await change_password(user, req['mat_khau_cu'], req['mat_khau_moi'])
#     if updated_password:
#         return ResponseModel(updated_password,'Thay đổi mật khẩu thành công')        
#     else:
#         return ErrorResponseModel(f"Mật khẩu cũ không đúng" , 409 ,"Lỗi")
    

# @router.put("/reset_password_user", summary= "Reset_password")
# async def reset_password(user = Depends(get_current_active_user)): 
    
#     check = userCollection.update_one({"ten_nguoi_dung": user['sub']}, {"$set": {'mat_khau':get_password_hash("B@ica0quen")}})
#     if check:
#         return ResponseModel("OK",'Reset mật khẩu thành công')        
#     else:
#         return ErrorResponseModel(f"Reset mật khẩu không thành công" , 409 ,"Lỗi")
