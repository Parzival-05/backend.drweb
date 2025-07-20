from flask_restx import abort, fields, Resource
from flask_restx._http import HTTPStatus
from app.db.base import db
from app.db.user import UserModel
from app.api_instance import api

ns_users = api.namespace("users", path="/api/users/", description="User operations")

user_model = ns_users.model(
    "user",
    {
        "id": fields.Integer(required=True, description="ID"),
        "email": fields.String(required=True, description="Email"),
    },
)

user_input_model = ns_users.model(
    "user_input",
    {
        "email": fields.String(required=True, description="Email"),
        "password": fields.String(required=True, description="Password"),
    },
)


class Users(Resource):
    @ns_users.marshal_with(user_model, as_list=True, description="List of users")
    @ns_users.doc(description="Get list of all users")
    def get(self):
        users = UserModel.query.all()
        return users

    @ns_users.expect(user_input_model)
    @ns_users.marshal_with(user_model, description="Registered user")
    @ns_users.doc(description="Register user")
    def post(self):
        args = api.payload
        if UserModel.query.filter_by(email=args["email"]).first() is not None:
            abort(HTTPStatus.BAD_REQUEST, message="User already exists")
        user = UserModel(email=args["email"])  # type: ignore https://github.com/microsoft/pylance-release/issues/6199
        user.hash_password(args["password"])
        db.session.add(user)
        db.session.commit()
        return user


class User(Resource):
    @ns_users.marshal_with(user_model, description="User")
    @ns_users.doc(description="Get user by id")
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(HTTPStatus.BAD_REQUEST, message=f"User with id={user_id} not found")
        return user
