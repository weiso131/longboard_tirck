
from bson import ObjectId

from fastapi import APIRouter

from schemas.trick import StudentTrick, StudentTrickUpdate
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


router = APIRouter(dependencies=[TeacherDepend])


@router.get("/")
async def show_all_student():
    students = await user_collection.find({"identity": 1}, {"_id": 0}).to_list()
    return students
@router.get("/check_student")
async def check_student(student_uid: str):
    check_user_exist(student_uid)
    student_trick = await student_collection.find({"uid": student_uid}, {"_id": 0}).to_list()
    return student_trick
@router.post("/check_student/add_trick")
async def add_trick(student_uid: str, trick: StudentTrick):
    check_user_exist(student_uid)
    #滑板是自由的運動，招式自創問題不大？
    if await student_collection.find_one({"name": trick.name}):
        raise TRICK_ALREADY_EXIST
    trick_dict = trick.model_dump()
    trick_dict['uid'] = student_uid
    await student_collection.insert_one(trick_dict)

    return {"status_code": True}
    
@router.put("/check_student/update_trick")
async def update_trick(student_uid: str, trick_update_data: StudentTrickUpdate):
    check_user_exist(student_uid)
    trick = await student_collection.find_one({"name": trick_update_data.name})
    if not trick:
        raise TRICK_NOT_EXIST
    trick_dict = trick_update_data.model_dump()
    trick_dict["name"] = trick_dict["new_name"]
    trick_dict.pop("new_name")

    update_data = {k: v for k, v in trick_dict.items() if v is not None}

    await student_collection.update_one(
        {"_id": ObjectId(trick["_id"])},
        {"$set": update_data}
    )

    return {"status_code": True}