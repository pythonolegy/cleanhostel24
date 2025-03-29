from http.client import HTTPException

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/rooms/")
def create_room(name: str, db: Session = Depends(get_db)):
    db_room = db.query(models.Room).filter(models.Room.name == name).first()
    if db_room:
        raise HTTPException(status_code=400, detail="Room already exists")

    new_room = models.Room(name=name)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@app.get("/rooms/")
def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(models.Room).all()
    return rooms