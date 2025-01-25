from fastapi import APIRouter
import bcrypt


from .utils.jwt import *
from schemas.user import UserUpdate, User
from exception import *


async def check_user_exist(uid):
    find = await User.find_one(User.uid == uid)
    if not find:
        raise USER_NOT_EXISTS
    return find

router = APIRouter()

@router.get('/get')
async def get_data(data=UserDepend):
    uid = data['uid']
    user = await User.find_one(User.uid == uid)
    if not user:
        raise USER_NOT_EXISTS
    user_dict = user.dict()
    user_dict.pop("id", None)
    return user_dict

@router.post('/update')
async def update(new_data: UserUpdate, data=UserDepend):
    uid = data["uid"]
    user = await check_user_exist(uid)
    
    await user.set(new_data.model_dump(exclude_none=True))

    return {"status_code": True}

@router.delete('/delete')
async def delete(password: str, data=UserDepend):
    uid = data['uid']
    user = await check_user_exist(uid)
    if not bcrypt.checkpw(password.encode(), user.password.encode("utf-8")):
        return WRONG_EMAIL_OR_PASSWORD
    await user.delete()
    return {"status_code": True}

