from flask import g

from app.db.user import UserModel


class AuthService:
    @staticmethod
    def get_authorized_user() -> UserModel:
        return g.user
