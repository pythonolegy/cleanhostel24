from fastapi import FastAPI
from sqladmin import Admin, ModelView

from .models import Room
from .database import engine

app = FastAPI()

admin = Admin(app, engine)

class RoomAdmin(ModelView, model=Room):
    column_list = ["id", "name", "status", "price", "image"]
    form_columns = ["name", "status", "price", "image"]

admin.add_view(RoomAdmin)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)