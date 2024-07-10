from prisma import Prisma

db = Prisma()

async def connect():
    await db.connect()

async def disconnect():
    await db.disconnect()
