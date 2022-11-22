from dao.user import UserDAO
from service.constans import PWD_HASH_SALT, PWD_HASH_ITERATIONS
import hashlib
import base64
import hmac


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data: dict[str, str]):
        username = data.get("username", None)
        password = data.get("password", None)
        role = data.get("role", None)

        if None in [username, password, role]:
            return {"error": "Не указаны все поля "}, 400

        user = self.get_user_by_username(username)

        if user is not None:
            return {"error": "Пользователь уже суещствует."}, 401

        password_hash = self.generate_pasword(password)
        user_data = {"username": username, "password": password_hash, "role": role}
        return self.dao.create(user_data)

    def update(self, data):
        self.dao.update(data)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def get_user_by_username(self, username: str):
        return self.dao.get_user_by_username(username)

    def generate_pasword(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), PWD_HASH_SALT, PWD_HASH_ITERATIONS
        )

        return base64.b64encode(hash_digest)

    def compare_passwords(self, password_hash, other_password_hash) -> bool:
        decoded_digest = base64.b64decode(password_hash)
        other_decoded_password = base64.b64decode(other_password_hash)
        return hmac.compare_digest(decoded_digest, other_decoded_password)