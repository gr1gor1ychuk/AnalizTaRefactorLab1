import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'lessonsss.db')}"
    SQLALCHEMY_BINDS = {
        'groups': f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'groups.db')}"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
