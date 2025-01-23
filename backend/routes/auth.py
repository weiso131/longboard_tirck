from fastapi import APIRouter
from .utils.jwt import *
import uuid


import bcrypt

from schemas.user import UserCreate

from exception import *

user_collection = None

def init_app(db):
    global user_collection
    user_collection = db['user']

router = APIRouter()

@router.post('/register')
async def register(data: UserCreate):
    hashpw = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
    uid = uuid.uuid4()
    find = await user_collection.find_one({"email": data.email})
    if find:
        return USER_ALREADY_EXISTS

    user = {
        "uid": str(uid),
        "name": str(data.name),
        "password": hashpw.decode("utf-8"),
        "email": str(data.email),
        "sex": bool(data.sex),
        "age": int(data.age),
        "identity": int(data.identity),
    }
    jwt_token = generate_tokens(user)

    await user_collection.insert_one(user)

    return jwt_token

@router.get('/login')
async def login(email: str, password: str):
    user = await user_collection.find_one({"email": email})
    if not user:
        return WRONG_EMAIL_OR_PASSWORD
    if not bcrypt.checkpw(password.encode(), user["password"].encode("utf-8")):
        return WRONG_EMAIL_OR_PASSWORD
    
    user.pop("_id", None)
    return generate_tokens(user)



@router.put('/refresh')
def refresh(data=UserDepend):
    return generate_tokens(data)