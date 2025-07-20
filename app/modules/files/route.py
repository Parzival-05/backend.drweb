from enum import StrEnum
import os
import shutil
from typing import Optional
from flask import send_file
from flask_restx._http import HTTPStatus
from flask_restx import abort, reqparse, fields, Resource
from werkzeug.datastructures import FileStorage

from app.api_instance import api
from app.db.base import db
from app.db.file import FileModel
from app.modules.auth.decorators import auth
from app.modules.auth.service import AuthService
from app.modules.decorator_utils import decorate_methods
from app.modules.files.service import FILE_STORAGE_PATH, StorageService

ns_files = api.namespace("files", path="/api/files/", description="File operations")

upload_file_parser = reqparse.RequestParser()
upload_file_parser.add_argument(
    "file", location="files", type=FileStorage, required=True
)

get_file_parser = reqparse.RequestParser()
get_file_parser.add_argument("file_hash", location="args", type=str, required=True)


file_model = ns_files.model(
    "file",
    {
        "file_hash": fields.String(required=True, description="File's hash"),
    },
)


class FileErrors(StrEnum):
    FILE_NOT_FOUND = "File not found"
    FILE_OWNERSHIP_ERROR = "File ownership error"


class Files(Resource):
    method_decorators = decorate_methods(
        post=[auth.login_required], delete=[auth.login_required]
    )

    @ns_files.expect(get_file_parser)
    @ns_files.doc(
        description="Downloads file by it's hash", produces=["application/octet-stream"]
    )
    def get(self):
        args = get_file_parser.parse_args()
        file_hash = args["file_hash"]
        file_model: Optional[FileModel] = FileModel.query.filter_by(
            file_hash=file_hash
        ).first()
        if file_model is None:
            abort(HTTPStatus.BAD_REQUEST, message=FileErrors.FILE_NOT_FOUND)
            return

        return send_file(
            StorageService.file_path(file_hash),
            download_name=file_model.filename,
            as_attachment=True,
        )

    @ns_files.expect(upload_file_parser)
    @ns_files.marshal_with(file_model, description="File hash")
    @ns_files.doc(description="Upload file")
    def post(self):
        user = AuthService.get_authorized_user()
        args = upload_file_parser.parse_args()
        file: FileStorage = args.file
        data = file.stream.read()  # TODO: support of big files
        file_hash = StorageService.hash_file(data, user_id=user.id)
        filename = file.name
        if (
            FileModel.query.filter_by(file_hash=file_hash, user_id=user.id).first()
            is not None
        ):
            abort(HTTPStatus.BAD_REQUEST, message="File is already exists")
        file_path = StorageService.file_path(file_hash)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        file.stream.seek(0)  # set cursor to the beginning
        file.save(file_path)
        file.close()

        file_model = FileModel(file_hash=file_hash, filename=filename, user_id=user.id)  # type: ignore
        db.session.add(file_model)
        db.session.commit()
        return file_model

    @ns_files.expect(file_model)
    @ns_files.response(HTTPStatus.OK, description="File deleted")
    @ns_files.doc(description="Deleted file by it's hash")
    def delete(self):
        user = AuthService.get_authorized_user()
        args = api.payload
        file_hash = args["file_hash"]
        file_model: Optional[FileModel] = FileModel.query.filter_by(
            file_hash=file_hash
        ).first()
        if file_model is None:
            abort(HTTPStatus.BAD_REQUEST, message=FileErrors.FILE_NOT_FOUND)
        elif file_model.user_id != user.id:
            abort(HTTPStatus.BAD_REQUEST, message=FileErrors.FILE_OWNERSHIP_ERROR)

        file_path = StorageService.file_path(file_hash)
        file_dir = os.path.dirname(file_path)
        if file_dir != FILE_STORAGE_PATH:  # for security reasons
            shutil.rmtree(os.path.dirname(file_path))
        db.session.delete(file_model)
        db.session.commit()
        return
