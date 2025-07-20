from flask import g

from flask_httpauth import HTTPBasicAuth

from app.db.user import UserModel

auth = HTTPBasicAuth()
auth_admin = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    user: UserModel = UserModel.query.filter_by(email=email).first()  # type: ignore
    if not user or not user.verify_password(password):
        return None
    g.user = user
    return user


@auth_admin.verify_password
def verify_admin(email, password):
    user: UserModel = UserModel.query.filter_by(email=email).first()  # type: ignore
    if (
        not user
        or not user.verify_password(password)
        or not user.email == "admin@gmail.com" # TODO: we need a better place for it
    ):
        return None
    g.user = user
    return user
