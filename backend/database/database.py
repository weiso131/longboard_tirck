from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from config import settings
from schemas.trick import Trick, StudentTrick
from schemas.user import User

async def init_database():
    dc_name = settings.dc_name
    uri = settings.uri
    tlsCAFileName = "mongodb-bundle.pem"
    client = AsyncIOMotorClient(uri, tlsCAFile=tlsCAFileName)
    db = client[dc_name]
    await init_beanie(database=db, 
                      document_models=[
                          User,
                          Trick,
                          StudentTrick,
                    ])
