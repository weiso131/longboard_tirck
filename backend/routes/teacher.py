
from bson import ObjectId

from fastapi import APIRouter

from schemas.trick import StudentTrickCreate, StudentTrickUpdate, StudentTrick, StudentTrickWithUid
from schemas.user import User, UserWithUid
from .utils.jwt import *
from .user import check_user_exist

from exception import *




router = APIRouter(dependencies=[TeacherDepend])


@router.get("/")
async def show_all_student():
    students = await User.find(User.identity == 1).project(UserWithUid).to_list()
    return students
@router.get("/check_student")
async def check_student(student_uid: str):
    check_user_exist(student_uid)
    student_trick = await StudentTrick.find(StudentTrick.uid == student_uid).project(StudentTrickWithUid).to_list()
    return student_trick
@router.post("/check_student/add_trick")
async def add_trick(student_uid: str, trick: StudentTrickCreate):
    check_user_exist(student_uid)
    #滑板是自由的運動，招式自創問題不大？
    if await StudentTrick.find_one(StudentTrick.name == trick.name):
        raise TRICK_ALREADY_EXIST
    trick_dict = trick.model_dump()
    trick_dict['uid'] = student_uid
    await StudentTrick.insert_one(StudentTrick(**trick_dict))

    return {"status_code": True}
    
@router.put("/check_student/update_trick")
async def update_trick(student_uid: str, trick_name: str, trick_update_data: StudentTrickUpdate):
    check_user_exist(student_uid)
    trick = await StudentTrick.find_one(StudentTrick.name == trick_name)
    if not trick:
        raise TRICK_NOT_EXIST
    await trick.set(trick_update_data.model_dump(exclude_none=True))

    return {"status_code": True}