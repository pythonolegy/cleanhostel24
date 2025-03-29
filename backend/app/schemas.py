from pydantic import BaseModel

class RoomBase(BaseModel):
    name: str
    status: bool
    price: float
    image: str

    class Config:
        orm_mode = True

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True
