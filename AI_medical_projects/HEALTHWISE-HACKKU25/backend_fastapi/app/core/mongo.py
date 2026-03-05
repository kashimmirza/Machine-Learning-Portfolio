from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[settings.DB_NAME]
        print("✅ FastAPI Connected to MongoDB")

    async def close(self):
        if self.client:
            self.client.close()
            print("🛑 FastAPI Disconnected from MongoDB")

db = Database()
