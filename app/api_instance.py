from flask_restx import Api


api = Api(
    version="1.0",
    title="File storage API",
    description="File storage API",
    validate=True,
)
