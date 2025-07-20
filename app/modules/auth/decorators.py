from flask import g

from flask_httpauth import HTTPBasicAuth

from app.db.user import UserModel

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    user: UserModel = UserModel.query.filter_by(email=email).first()  # type: ignore
    if not user or not user.verify_password(password):
        return None
    g.user = user
    return user
