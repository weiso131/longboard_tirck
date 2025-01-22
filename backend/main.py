from fastapi import FastAPI
from routes import auth, user
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from routes import init_app

dc_name = settings.dc_name
uri = settings.uri
tlsCAFileName = "mongodb-bundle.pem"
client = AsyncIOMotorClient(uri, tlsCAFile=tlsCAFileName)
db = client[dc_name]

init_app(db)

app = FastAPI()
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")