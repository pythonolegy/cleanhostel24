from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware

from .admin import init_admin
from . import crud, schemas
from .database import async_session_maker, init_db


app = FastAPI()

# Разрешаем запросы с фронта (замени на актуальный порт, если у тебя другой)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация базы данных при старте приложения
@app.on_event("startup")
async def on_startup():
    await init_db()  # Асинхронный вызов инициализации базы данных

init_admin(app)  # Инициализация админки

# Заменяем Session на асинхронную сессию
async def get_db():
    db = async_session_maker()
    try:
        yield db
    finally:
        await db.close()  # Закрытие асинхронной сессии

@app.get("/rooms/", response_model=list[schemas.Room])
async def read_rooms(db: AsyncSession = Depends(get_db)):
    rooms = await crud.get_rooms(db=db)  # асинхронный вызов
    return rooms

@app.get("/rooms/{room_id}", response_model=schemas.Room)
async def read_room(room_id: int, db: AsyncSession = Depends(get_db)):
    db_room = await crud.get_room(db, room_id=room_id)  # асинхронный вызов
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@app.post("/rooms/", response_model=schemas.Room)
async def create_room(room: schemas.RoomCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_room(db=db, room=room)  # асинхронный вызов

@app.put("/rooms/{room_id}", response_model=schemas.Room)
async def update_room(room_id: int, room: schemas.RoomUpdate, db: AsyncSession = Depends(get_db)):
    db_room = await crud.get_room(db, room_id=room_id)  # асинхронный вызов
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return await crud.update_room(db=db, room_id=room_id, room=room)  # асинхронный вызов

@app.delete("/rooms/{room_id}", response_model=schemas.Room)
async def delete_room(room_id: int, db: AsyncSession = Depends(get_db)):
    db_room = await crud.get_room(db, room_id=room_id)  # асинхронный вызов
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return await crud.delete_room(db=db, room_id=room_id)  # асинхронный вызов

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)