import hashlib
from os import PathLike
import os
import uuid

from pydantic import BaseModel

from app.config.config import FILE_STORAGE_PATH, TEMP_FILE_STORAGE_PATH

CHUNK_SIZE = 16 * 1024


class ProcessedFile(BaseModel):
    file_hash: str
    temp_file_path: PathLike


class StorageService:
    @staticmethod
    def process_stream(stream) -> ProcessedFile:
        sha256_hash = hashlib.sha256()
        uuid_v = uuid.uuid4()
        temp_file_path = StorageService.file_path_temp(uuid_v)
        try:
            with open(temp_file_path, "wb") as temp_file:
                for file_content in StorageService.read_file_chunks(stream):
                    sha256_hash.update(file_content)
                    temp_file.write(file_content)

            return ProcessedFile(
                file_hash=sha256_hash.hexdigest(), temp_file_path=temp_file_path
            )
        except Exception:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise

    @staticmethod
    def file_path(file_hash: str) -> PathLike:
        return FILE_STORAGE_PATH / f"{file_hash[:2]}" / file_hash

    @staticmethod
    def file_path_temp(uuid: uuid.UUID) -> PathLike:
        return TEMP_FILE_STORAGE_PATH / str(uuid)

    @staticmethod
    def read_file_chunks(stream):
        while True:
            buf = stream.read(CHUNK_SIZE)
            if buf:
                yield buf
            else:
                break
