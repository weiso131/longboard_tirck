from fastapi import APIRouter

from schemas.trick import TrickBase, TrickUpdate, Trick
from .utils.jwt import *
from .user import check_user_exist

from exception import *

router = APIRouter()

@router.post("/add_trick")
async def add_trick(trick: TrickBase, teacher=TeacherDepend):
    check_user_exist(teacher["uid"])

    trick_dict = trick.model_dump()
    if await Trick.find_one(Trick.name == trick_dict["name"]):
        raise TRICK_ALREADY_EXIST
    await Trick.insert_one(Trick(**trick_dict))

    return {"status_code": True}

@router.get("/list")
async def trick_list():
    all_trick = await Trick.find_all().project(TrickBase).to_list()
    return all_trick

@router.put("/update")
async def trick_update(trick_name: str, trick_update_data: TrickUpdate, teacher=TeacherDepend):
    check_user_exist(teacher["uid"])
    
    trick = await Trick.find_one(Trick.name == trick_name)
    if not trick:
        raise TRICK_NOT_EXIST

    await trick.set(trick_update_data.model_dump(exclude_none=True))
    return {"status": True}


