from fastapi import APIRouter

user_collection = None

def init_app(db):
    global user_collection
    user_collection = db['user']


router = APIRouter()

