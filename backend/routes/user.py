from fastapi import APIRouter
from .utils.jwt import *
from schemas.user import UserUpdate

user_collection = None

USER_NOT_EXISTS = HTTPException(
    status_code=400,
    detail="The account isn't exist"
)

def init_app(db):
    global user_collection
    user_collection = db['user']

async def check_user_exist(user):
    uid = user["uid"]
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
    
    check_user_exist(data)
    uid = data["uid"]
    update_data = {k: v for k, v in new_data.model_dump().items() if v is not None}

    await user_collection.update_one(
        {"uid": uid},
        {"$set": update_data}
    )

    return {"status_code": True}

@router.delete('/delete')
async def delete(password: str, data=UserDepend):
    uid = data['uid']
    find = await user_collection.find_one({"uid": uid})
    if not find:
        raise USER_NOT_EXISTS
    await user_collection.delete_one({"uid": uid})
    return {"status_code": True}

