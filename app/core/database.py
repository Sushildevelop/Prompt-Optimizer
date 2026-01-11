from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings


import asyncio


class Database:
    client: AsyncIOMotorClient = None
    database = None


database = Database()


async def connect_to_mongo():
    """Create database connection"""
    database.client = AsyncIOMotorClient(settings.mongodb_url)
    database.database = database.client[settings.database_name]
    
    # Initialize Beanie with the models
    await init_beanie(
        database=database.database,
        document_models=[])


async def close_mongo_connection():
    """Close database connection"""
    if database.client:
        database.client.close()


async def get_database():
    """Get database instance"""
    return database.database