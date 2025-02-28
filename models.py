# models.py
from config import db1


class User(db1.Model):
    __tablename__ = "users"

    id = db1.Column(db1.Integer, primary_key=True)
    username = db1.Column(db1.String, unique=True, nullable=False)
    password = db1.Column(db1.String, nullable=False)
    created_at = db1.Column(db1.DateTime, server_default=db1.func.now())
