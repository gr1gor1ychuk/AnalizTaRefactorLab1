# routes.py
from http import HTTPStatus

from flask import Blueprint, request, jsonify, render_template
from models import db
from models import Lessons, Groups
from utils import order_lessons, lessons_to_dict

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
def home():
    return render_template('index.html')


@routes_bp.route('/schedule')
def schedule():
    ordered_lessons = order_lessons(Lessons.query)
    lessons_dict = {}

    for lesson in ordered_lessons:
        if lesson.day not in lessons_dict:
            lessons_dict[lesson.day] = []
        lessons_dict[lesson.day].append(lesson)

    return render_template("calendar.html", schedule_dict=lessons_dict)


@routes_bp.route("/lessons", methods=["GET"])
def get_all_lessons():
    ordered_lessons = order_lessons(Lessons.query)
    return jsonify(lessons_to_dict(ordered_lessons)), HTTPStatus.OK


@routes_bp.route("/lessons/teacher/<teacher_name>", methods=["GET"])
def get_lessons_by_teacher(teacher_name):
    teacher_lessons = Lessons.query.filter_by(teacher=teacher_name).all()
    return jsonify(lessons_to_dict(order_lessons(teacher_lessons))), HTTPStatus.OK


@routes_bp.route("/lessons/academic-group/<academic_group>", methods=["GET"])
def get_lessons_by_academic_group(academic_group):
    group_lessons = Lessons.query.filter_by(academic_group=academic_group).all()
    return jsonify(lessons_to_dict(order_lessons(group_lessons))), HTTPStatus.OK


@routes_bp.route("/lessons/add", methods=["POST"])
def add_lesson():
    data = request.form
    try:
        new_lesson = Lessons(
            teacher=data["teacher"],
            academic_group=data["academic_group"],
            subject=data["subject"],
            day=data["day"],
            class_order=int(data["class_order"])
        )
        db.session.add(new_lesson)
        db.session.commit()
        return jsonify({"message": "Lesson added successfully"}), HTTPStatus.CREATED
    except ImportError as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST


@routes_bp.route("/lessons/delete/<int:lesson_id>", methods=["DELETE"])
def delete_lesson(lesson_id):
    lesson = Lessons.query.get(lesson_id)
    if lesson:
        db.session.delete(lesson)
        db.session.commit()
        return jsonify({"message": "Lesson deleted successfully"}), HTTPStatus.OK
    return jsonify({"error": "Lesson not found"}), HTTPStatus.NOT_FOUND


@routes_bp.route("/lessons/edit/<int:lesson_id>", methods=["PUT"])
def edit_lesson(lesson_id):
    lesson = Lessons.query.get(lesson_id)
    if lesson:
        try:
            lesson.teacher = request.form["teacher"]
            lesson.academic_group = request.form["academic_group"]
            lesson.subject = request.form["subject"]
            lesson.day = request.form["day"]
            lesson.class_order = int(request.form["class_order"])

            db.session.commit()
            return jsonify({"message": "Lesson edited successfully"}), HTTPStatus.OK
        except ImportError as e:
            return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    return jsonify({"error": "Lesson not found"}), HTTPStatus.NOT_FOUND


@routes_bp.route("/group-info/<group_name>", methods=["GET"])
def get_group_info(group_name):
    group = Groups.query.filter_by(group_name=group_name).first()
    return jsonify({"starosta": group.starosta, "contact_starosta": group.contact_starosta}) \
        if group else jsonify({"error": "Group not found"}), HTTPStatus.NOT_FOUND


@routes_bp.route("/group-list", methods=["GET"])
def get_group_list():
    groups = Groups.query.all()
    return jsonify([{"group_name": group.group_name} for group in groups]), HTTPStatus.OK
