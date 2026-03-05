from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.logging import logger

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGO_URI)
            self.db = self.client[settings.MONGO_DB_NAME]
            # Ping to verify
            await self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB.")
        except Exception as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise e

    async def close(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

mongo_db = MongoDB()
