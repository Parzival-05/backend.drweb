from app.db.base import db


class FileModel(db.Model):
    __tablename__ = "file"

    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))