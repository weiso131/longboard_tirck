from fastapi import APIRouter
import bcrypt


from .utils.jwt import *
from schemas.user import UserUpdate
from exception import *

user_collection = None


def init_app(db):
    global user_collection
    user_collection = db['user']

async def check_user_exist(uid):
    find = await user_collection.find_one({"uid": uid})
    if not find:
        raise USER_NOT_EXISTS

router = APIRouter()

@router.get('/get')
async def get_data(data=UserDepend):
    uid = data['uid']
    user = await user_collection.find_one({"uid": uid})
    if not user:
        raise USER_NOT_EXISTS
    user.pop("_id", None)
    return user

@router.post('/update')
async def update(new_data: UserUpdate, data=UserDepend):
    uid = data["uid"]
    check_user_exist(uid)
    
    update_data = {k: v for k, v in new_data.model_dump().items() if v is not None}

    await user_collection.update_one(
        {"uid": uid},
        {"$set": update_data}
    )

    return {"status_code": True}

@router.delete('/delete')
async def delete(password: str, data=UserDepend):
    uid = data['uid']
    user = await user_collection.find_one({"uid": uid})
    if not user:
        raise USER_NOT_EXISTS
    if not bcrypt.checkpw(password.encode(), user["password"].encode("utf-8")):
        return WRONG_EMAIL_OR_PASSWORD
    await user_collection.delete_one({"uid": uid})
    return {"status_code": True}

