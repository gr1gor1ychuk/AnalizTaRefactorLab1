import json
from flask import current_app
from models import db, Lessons, Groups


def parse_to_db_groups():
    with current_app.app_context():
        with open("groups.json", "r", encoding="utf-8") as file:
            groups_data = json.load(file)
            for group_info in groups_data["groups"]:
                db.session.add(Groups(**group_info))

        db.create_all()
        db.session.commit()


def parse_to_db():
    with current_app.app_context():
        with open("lessons.json", "r", encoding="utf-8") as file:
            lessons_data = json.load(file)
            for lesson_info in lessons_data["lessons"]:
                db.session.add(Lessons(**lesson_info))

        db.create_all()
        db.session.commit()
