from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Lessons(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher = db.Column(db.String(200), nullable=False)
    academic_group = db.Column(db.String(10), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    class_order = db.Column(db.Integer, nullable=False)


class Groups(db.Model):
    __bind_key__ = 'groups'
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(10), nullable=False)
    starosta = db.Column(db.String(200), nullable=False)
    contact_starosta = db.Column(db.String(200), nullable=False)
