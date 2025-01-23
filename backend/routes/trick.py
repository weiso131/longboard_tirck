
from bson import ObjectId

from fastapi import APIRouter

from schemas.trick import Trick, TrickUpdate
from .utils.jwt import *
from .user import check_user_exist

from exception import *


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
async def add_trick(trick: Trick, teacher=TeacherDepend):
    check_user_exist(teacher["uid"])

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
async def trick_update(trick_update_data: TrickUpdate, teacher=TeacherDepend):
    check_user_exist(teacher["uid"])
    
    trick_dict = trick_update_data.model_dump()
    trick_dict["name"] = trick_dict["new_name"]
    trick_dict.pop("new_name")
    trick = await trick_collection.find_one({"name": trick_update_data.name})
    if not trick:
        raise TRICK_NOT_EXIST

    update_data = {k: v for k, v in trick_dict.items() if v is not None}

    await trick_collection.update_one(
        {"_id": ObjectId(trick["_id"])},
        {"$set": update_data}
    )
    return {"status": True}


