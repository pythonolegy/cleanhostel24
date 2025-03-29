from sqlalchemy.orm import Session
from . import models, schemas

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name, status=room.status, price=room.price, image=room.image)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()

def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def update_room(db: Session, room_id: int, room: schemas.RoomUpdate):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room:
        db_room.name = room.name
        db_room.status = room.status
        db_room.price = room.price
        db_room.image = room.image
        db.commit()
        db.refresh(db_room)
        return db_room
    return None

def delete_room(db: Session, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room:
        db.delete(db_room)
        db.commit()
    return db_room