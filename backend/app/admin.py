from sqladmin import Admin, ModelView
import bcrypt
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from .database import engine, async_session_maker
from .models import Room, User
from .crud import get_user_by_username


class AdminAuth(AuthenticationBackend):
    @classmethod
    def verify_password(cls, password: str, user_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), user_password.encode())

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        async with async_session_maker() as db:
            user = await get_user_by_username(db, username)
            if not user:
                return False
            user_password = user.password

        if self.verify_password(password, user_password):
            request.session.update({"token": "valid_token"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("token") == "valid_token"


def init_admin(app):
    authentication_backend = AdminAuth(secret_key="test")
    admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend, base_url="/admin")

    class RoomAdmin(ModelView, model=Room):
        column_list = ["id", "name", "status", "price", "image"]
        form_columns = ["name", "status", "price", "image"]

    admin.add_view(RoomAdmin)
