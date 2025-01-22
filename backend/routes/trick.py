
from bson import ObjectId

from fastapi import APIRouter, HTTPException

from schemas.trick import Trick, TrickUpdate, StudentTrick
from .utils.jwt import *
from .user import check_user_exist

TRICK_ALREADY_EXIST = HTTPException(
    status_code=400, 
    detail="Trick already exist"
)

TRICK_NOT_EXIST = HTTPException(
    status_code=400, 
    detail="Trick not exist"
)
USER_NOT_EXISTS = HTTPException(
    status_code=400,
    detail="The account isn't exist"
)
STUDENT_NOT_ALLOW_EDIT_TRICK = HTTPException(
    status_code=400,
    detail="Student not allow to edit /trick"
)

user_collection = None
trick_collection = None
student_collection = None
def init_app(db):
    global user_collection, trick_collection, student_collection
    user_collection = db['user']
    trick_collection = db['trick']
    student_collection = db['student']


router = APIRouter()


@router.post("/add_trick")
async def add_trick(trick: Trick, teacher=UserDepend):
    check_user_exist(teacher)
    if teacher['identity'] == 1:
        raise STUDENT_NOT_ALLOW_EDIT_TRICK

    trick_dict = trick.model_dump()
    if await trick_collection.find_one({"name": trick_dict["name"]}):
        raise TRICK_ALREADY_EXIST
    await trick_collection.insert_one(trick_dict)

    return {"status_code": True}

@router.get("/list")
async def trick_list():
    all_trick = await trick_collection.find({}, {"_id": 0}).to_list(length=None)
    return all_trick

@router.put("/update")
async def trick_update(trick_update_data: TrickUpdate, teacher=UserDepend):
    check_user_exist(teacher)
    if teacher['identity'] == 1:
        raise STUDENT_NOT_ALLOW_EDIT_TRICK
    
    data_dict = trick_update_data.model_dump()
    data_dict["name"] = data_dict["new_name"]
    data_dict.pop("new_name")
    trick = await trick_collection.find_one({"name": trick_update_data.name})
    if not trick:
        raise TRICK_NOT_EXIST

    update_data = {k: v for k, v in data_dict.items() if v is not None}

    await trick_collection.update_one(
        {"_id": ObjectId(trick["_id"])},
        {"$set": update_data}
    )
    return {"status": True}


