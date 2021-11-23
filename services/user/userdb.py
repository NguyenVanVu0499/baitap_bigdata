from database.mongo import database
import re
from passlib.context import CryptContext
from bson.objectid import ObjectId
from datetime import date
today = date.today()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
userCollection = database.get_collection("nguoi_dung")
"""
=================================================
    DEFINE RETURN TYPE FOR USER
=================================================
"""
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "ten_nguoi_dung" : user["ten_nguoi_dung"],
        "ten_day_du" :user["ten_day_du"],
        "so_dien_thoai" :user["so_dien_thoai"],
        "email" :user["email"],
        "anh_dai_dien" :user["anh_dai_dien"],
        "ngay_tao": user["ngay_tao"],
        "trang_thai": user["trang_thai"],
    }


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = userCollection.find_one({
        'ten_nguoi_dung' : username,
    }) 
    if not verify_password(password, user['mat_khau']):
        return False
    
    return True


"""
=================================================
    Create User
    return 2 : user_existed,
    return 3 : insert success.
=================================================
"""
# async def create_user(new_user: dict, current_user)->dict:
async def create_user(new_user: dict)->dict:

    elecbid = await connect_bid_db()
    name = new_user['ten_nguoi_dung']
    user_existed = await elecbid.user.find_one({"ten_nguoi_dung":name}) 
    
    if user_existed:
        return 2
    else:
        new_user['mat_khau'] = get_password_hash(new_user['mat_khau'])
        new_user['ngay_tao'] = '{}'.format(today)
        new_user['trang_thai'] = True
        new_user['ten_nguoi_dung'] = new_user['ten_nguoi_dung'].lower()

        user = await elecbid.user.insert_one(new_user)
        # user_inserted = await elecbid.user.find_one({"_id":user.inserted_id})
        return 3


"""
=================================================
     Get all information user with pagination
        - page_size : Size of information display on screen.
        - page_num : number of page.
        - skips : when you wanna load page 2 we skip 10 first element and display from 11 to 20.
=================================================
"""
async def get_all_user(current_user, user_name, page_size:int = 10, page_num:int = 1):

    query = {}
    regx = re.compile("{}".format(user_name), re.IGNORECASE)
    if user_name != None:
        query['ten_nguoi_dung'] = regx
    
    if current_user['rolename'] != "Quản trị viên":
        role_ids = []
        query1 = {}
        regxstr = re.compile(".*{}.*".format(current_user['roleid']), re.IGNORECASE)
        query1['path'] = regxstr

        for n in roleCollection.find(query1):
            role_ids.append(str(n['_id']))
        role_ids.append(current_user['roleid'])

        query['ma_quyen_nguoi_dung'] = {'$in': role_ids}
    user_info = []
    
    # Calculate number of documents to skip
    skips = page_size * (page_num - 1)
    for n in userCollection.find(query).skip(skips).limit(page_size):
        user_info.append(user_helper(n))
    total_count = userCollection.count(query)
    
    user_data = {
        "users_info" : user_info,
        "total" : total_count
    }
    return user_data


async def update_user(user_id :str, data_update_user: dict):
    """
        Update a user with UserId.
    """
    # Return false if an empty request body is sent.
    if len(data_update_user) < 1:
        return False
    user = userCollection.find_one({"_id": ObjectId(user_id)})
    if user:
        name = data_update_user["ten_nguoi_dung"]        
        user_existed = userCollection.find_one({"user_name":name})
        if user_existed:
            return 2
        else:
            ma_chuc_vu = data_update_user["ma_chuc_vu"] 
            chuc_vu = cv_Collection.find_one({"_id":ObjectId(ma_chuc_vu)})
            data_update_user['ten_chuc_vu'] = chuc_vu['ten'] 
            data_update_user['ngay_tao'] = '{}'.format(today)
            data_update_user['trang_thai'] = True
            data_update_user['ten_nguoi_dung'] = data_update_user['ten_nguoi_dung'].lower()
            updated_user = userCollection.update_one({"_id": ObjectId(user_id)}, {"$set": data_update_user})            
            if updated_user:
                return 3
    else:
        return {"error":"not found any user"}


async def delete_user(id:str, force: bool):
    """
        If force is True delete user.
        else update status user .
    """

    if force:
        return userCollection.delete_one({"_id":ObjectId(id)}) 
    else:
        return userCollection.update_one({'_id':ObjectId(id)},{'$set':{'trang_thai': False }})


async def change_password(user, mat_khau_cu :str, mat_khau_moi: str):
    if mat_khau_cu != None and authenticate_user(user['sub'], mat_khau_cu):
        if userCollection.update_one({"ten_nguoi_dung": user['sub']}, {"$set": {'mat_khau':get_password_hash(mat_khau_moi)}}):
            return True
    return False
    


    