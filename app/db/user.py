from app.db.base import db

from passlib.apps import custom_app_context as pwd_context


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    files = db.relationship("FileModel", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"User(id={self.id}, email={self.email})"

    def hash_password(self, password):
        self.password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    # def generate_auth_token(self, expiration=600):
    #     s = Serializer(app.config["SECRET_KEY"])
    #     return s.dumps({"id": self.id})

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(app.config["SECRET_KEY"])
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None  # valid token, but expired
    #     except BadSignature:
    #         return None  # invalid token
    #     user = UserModel.query.get(data["id"])
    #     return user
