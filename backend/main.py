from contextlib import asynccontextmanager

from fastapi import FastAPI
from routes import auth, user, trick, teacher

from database.database import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("初始化資料庫")
    await init_database()
    yield
    print("關閉應用")
    


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")
app.include_router(trick.router, prefix="/trick")
app.include_router(teacher.router, prefix="/teacher")

