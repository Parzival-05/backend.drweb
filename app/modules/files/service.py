import hashlib
from os import PathLike

from app.config.config import FILE_STORAGE_PATH


class StorageService:
    @staticmethod
    def hash_file(file_content: bytes, user_id: int) -> str:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(file_content)
        sha256_hash.update(str(user_id).encode("utf-8"))
        return sha256_hash.hexdigest()

    @staticmethod
    def file_path(file_hash: str) -> PathLike:
        return FILE_STORAGE_PATH / f"{file_hash[:2]}/{file_hash}"
