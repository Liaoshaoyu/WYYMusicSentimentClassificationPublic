from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

from models.admin import Admin
from models.student import Student
from models.wang_yi_yun import SongCommentsData, CommentLengthData, WordCloudData


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None

    # JWT
    secret_key: str = 'guiyfgc837tgf3iw87-012389764'
    algorithm: str = "HS256"

    class Config:
        env_file = ".env.dev"
        orm_mode = True


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(
        # database=client.get_default_database(),
        database=client['WangYiYun'],
        document_models=[SongCommentsData, CommentLengthData, WordCloudData])
