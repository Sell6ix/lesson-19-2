import hashlib
import calendar
import datetime

from service.implemented import UserService
from service.constans import PWD_HASH_SALT  as SECRET, PWD_HASH_ALGO as ALGO
import jwt


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def auth(self, data: dict[str, str]):
        username = data.get("username", None)
        password = data.get("password", None)

        user = self.user_service.get_user_by_username(username)

        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        password_hash = self.user_service.generate_pasword(password)

        if self.user_service.compare_passwords(password_hash, user.password) == False:
            return {"error": "Неправильный пароль"}, 401

        return self._generate_token(user.username, user.password)

    def refresh_token(self, refresh_token: str):
        try:
            data = jwt.decode(jwt=refresh_token, key=SECRET, algorithms=[ALGO])
        except Exception as e:
            return {"error": "Bad request"}, 400

        username = data.get("username")

        user = self.user_service.get_user_by_username(username)
        if user is None:
            return {"error": "Bad request"}, 400

        return self._generate_token(user.username, user.password)

    def validate_token(self, token: str) -> None:
        jwt.decode(token, SECRET, algorithms=[ALGO])

    def validate_admin_token(self, token: str) -> bool:
        try:
            data = jwt.decode(token, SECRET, algorithms=[ALGO])
            if "role" in data:
                return data["role"].lower() == "admin"
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
        return False

    # Private

    def _generate_token(self, username: str, password: str):
        user = self.user_service.get_user_by_username(username)

        if user is None:
            return {"error": "Пользователь не найден"}, 404

        if not self.user_service.compare_passwords(user.password, password):
            return {"error": "Пользователь не прошел авторизацию"}, 401

        data = {"username": user.username, "role": user.role}

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGO)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201