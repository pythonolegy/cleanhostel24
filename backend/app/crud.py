from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(models.User.name == username))
    return result.scalars().first()

# Создание комнаты
async def create_room(db: AsyncSession, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name, status=room.status, price=room.price, image=room.image)
    db.add(db_room)
    await db.commit()  # асинхронная коммит
    await db.refresh(db_room)  # асинхронный refresh
    return db_room

# Получение списка комнат
async def get_rooms(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Room).offset(skip).limit(limit))
    return result.scalars().all()

# Получение комнаты по id
async def get_room(db: AsyncSession, room_id: int):
    result = await db.execute(select(models.Room).filter(models.Room.id == room_id))
    return result.scalars().first()

# Обновление информации о комнате
async def update_room(db: AsyncSession, room_id: int, room: schemas.RoomUpdate):
    result = await db.execute(select(models.Room).filter(models.Room.id == room_id))
    db_room = result.scalars().first()
    if db_room:
        db_room.name = room.name
        db_room.status = room.status
        db_room.price = room.price
        db_room.image = room.image
        await db.commit()  # асинхронный коммит
        await db.refresh(db_room)  # асинхронный refresh
        return db_room
    return None

# Удаление комнаты
async def delete_room(db: AsyncSession, room_id: int):
    result = await db.execute(select(models.Room).filter(models.Room.id == room_id))
    db_room = result.scalars().first()
    if db_room:
        await db.delete(db_room)  # асинхронное удаление
        await db.commit()  # асинхронный коммит
    return db_room
