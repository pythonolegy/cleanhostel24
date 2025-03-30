from fastapi import FastAPI
from sqladmin import Admin, ModelView
import bcrypt
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from .crud import get_user_by_username
from .main import get_db
from .models import Room, User
from .database import engine


class AdminAuth(AuthenticationBackend):

    @classmethod
    def verify_password(cls, password: str, user_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), user_password.encode())

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        user, user_password = None, None

        async for db in get_db():
            user = await get_user_by_username(db, username)
            if not user:
                return False
            user_password = user.password
            break

        if user and self.verify_password(password, user_password):
            request.session.update({"token": "valid_token"})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        # Очистка сессии
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        return token == "valid_token"


app = FastAPI()

# Настройка аутентификации и админки
authentication_backend = AdminAuth(secret_key="test")
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

class RoomAdmin(ModelView, model=Room):
    column_list = ["id", "name", "status", "price", "image"]
    form_columns = ["name", "status", "price", "image"]

admin.add_view(RoomAdmin)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
