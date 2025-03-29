from fastapi import FastAPI, Depends
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from .models import Room
from .database import engine


# Создаем класс для аутентификации
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Простейшая проверка пользователя и пароля
        if username == "admin" and password == "admin123":
            # Обновление сессии (например, можно использовать токен)
            request.session.update({"token": "valid_token"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        # Очистка сессии
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        # Проверка токена в сессии
        token = request.session.get("token")
        return token == "valid_token"


# Создание приложения FastAPI
app = FastAPI()

# Настройка аутентификации и админки
authentication_backend = AdminAuth(secret_key="test")
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

# Создание модели админки для Room
class RoomAdmin(ModelView, model=Room):
    column_list = ["id", "name", "status", "price", "image"]
    form_columns = ["name", "status", "price", "image"]

# Добавление представления в админку
admin.add_view(RoomAdmin)

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
