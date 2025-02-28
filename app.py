from flask import Flask, request, jsonify, json, render_template
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lessonsss.db'
app.config['SQLALCHEMY_BINDS'] = {
    'groups': 'sqlite:///groups.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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


def parseToDBGroups():
    with app.app_context():
        with open("groups.json", "r") as file:
            groups_data = json.load(file)
            for group_info in groups_data["groups"]:
                group = Groups(**group_info)
                print(f"Adding group: {group_info}")
                db.session.add(group)

        db.create_all()

        db.session.commit()


def parseToDB():
    with app.app_context():
        with open("lessons.json", "r") as file:
            lessons_data = json.load(file)
            for lesson_info in lessons_data["lessons"]:
                lesson = Lessons(**lesson_info)
                db.session.add(lesson)

        db.create_all()

        db.session.commit()


Swagger(app)


def order_lessons(lessons):
    return sorted(
        lessons,
        key=lambda lesson: (
            {
                'Monday': 1,
                'Tuesday': 2,
                'Wednesday': 3,
                'Thursday': 4,
                'Friday': 5,
                'Saturday': 6,
            }.get(lesson.day, 99),
            lesson.class_order
        )
    )


def lessons_to_dict(lessons):
    return [
        {
            "id": lesson.id,
            "teacher": lesson.teacher,
            "academic_group": lesson.academic_group,
            "subject": lesson.subject,
            "day": lesson.day,
            "class_order": lesson.class_order
        }
        for lesson in lessons
    ]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/schedule')
def schedule():
    ordered_lessons = order_lessons(Lessons.query)
    lessons_dict = {}

    for lesson in ordered_lessons:
        if lesson.day not in lessons_dict:
            lessons_dict[lesson.day] = []
        lessons_dict[lesson.day].append(lesson)

    return render_template("calendar.html", schedule_dict=lessons_dict)


@app.route("/lessons", methods=["GET"])
def get_all_lessons():
    """
    Get all lessons.
    ---
    responses:
      200:
        description: A list of all lessons
    """
    ordered_lessons = order_lessons(Lessons.query)
    lessons_list = lessons_to_dict(ordered_lessons)

    return jsonify(lessons_list), 200


@app.route("/lessons/teacher/<teacher_name>", methods=["GET"])
def get_lessons_by_teacher(teacher_name):
    """
    Get lessons by teacher.
    ---
    parameters:
      - name: teacher_name
        in: path
        type: string
        required: true
        description: The name of the teacher
    responses:
      200:
        description: A list of lessons taught by the specified teacher
    """
    teacher_lessons = Lessons.query.filter_by(teacher=teacher_name).all()
    ordered_teacher_lessons = order_lessons(teacher_lessons)
    teacher_lessons_list = lessons_to_dict(ordered_teacher_lessons)

    return jsonify(teacher_lessons_list), 200


@app.route("/lessons/academic-group/<academic_group>", methods=["GET"])
def get_lessons_by_academic_group(academic_group):
    """
    Get lessons by academic group.
    ---
    parameters:
      - name: academic_group
        in: path
        type: string
        required: true
        description: The academic group
    responses:
      200:
        description: A list of lessons for the specified academic group
    """
    group_lessons = Lessons.query.filter_by(academic_group=academic_group).all()
    ordered_group_lessons = order_lessons(group_lessons)
    group_lessons_list = lessons_to_dict(ordered_group_lessons)

    return jsonify(group_lessons_list), 200


@app.route("/lessons/add", methods=["POST"])
def add_lesson():
    """
    Add a new lesson to the database.
    ---
    parameters:
      - name: teacher
        in: formData
        type: string
        required: true
        description: The name of the teacher
      - name: academic_group
        in: formData
        type: string
        required: true
        description: The academic group
      - name: subject
        in: formData
        type: string
        required: true
        description: The subject of the lesson
      - name: day
        in: formData
        type: string
        required: true
        description: The day of the week
      - name: class_order
        in: formData
        type: integer
        required: true
        description: The order of the class
    responses:
      201:
        description: Lesson added successfully
      400:
        description: Bad request, check your input data
    """
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
        return jsonify({"message": "Lesson added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/lessons/delete/<int:lesson_id>", methods=["DELETE"])
def delete_lesson(lesson_id):
    """
    Delete a lesson by ID.
    ---
    parameters:
      - name: lesson_id
        in: path
        type: integer
        required: true
        description: The ID of the lesson to delete
    responses:
      200:
        description: Lesson deleted successfully
      404:
        description: Lesson not found
    """
    lesson = Lessons.query.get(lesson_id)

    if lesson:
        db.session.delete(lesson)
        db.session.commit()
        return jsonify({"message": "Lesson deleted successfully"}), 200
    else:
        return jsonify({"error": "Lesson not found"}), 404


@app.route("/lessons/edit/<int:lesson_id>", methods=["PUT"])
def edit_lesson(lesson_id):
    """
    Edit a lesson by ID.
    ---
    parameters:
      - name: lesson_id
        in: path
        type: integer
        required: true
        description: The ID of the lesson to edit
      - name: teacher
        in: formData
        type: string
        required: true
        description: The name of the teacher
      - name: academic_group
        in: formData
        type: string
        required: true
        description: The academic group
      - name: subject
        in: formData
        type: string
        required: true
        description: The subject of the lesson
      - name: day
        in: formData
        type: string
        required: true
        description: The day of the week
      - name: class_order
        in: formData
        type: integer
        required: true
        description: The order of the class
    responses:
      200:
        description: Lesson edited successfully
      400:
        description: Bad request, check your input data
      404:
        description: Lesson not found
    """
    lesson = Lessons.query.get(lesson_id)

    if lesson:
        try:
            lesson.teacher = request.form["teacher"]
            lesson.academic_group = request.form["academic_group"]
            lesson.subject = request.form["subject"]
            lesson.day = request.form["day"]
            lesson.class_order = int(request.form["class_order"])

            db.session.commit()
            return jsonify({"message": "Lesson edited successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "Lesson not found"}), 404


@app.route("/group-info/<group_name>", methods=["GET"])
def get_group_info(group_name):
    """
    Get group info by group name.
    ---
    parameters:
      - name: group_name
        in: path
        type: string
        required: true
        description: The name of the group
    responses:
      200:
        description: Group info retrieved successfully
      404:
        description: Group not found
    """
    group = Groups.query.filter_by(group_name=group_name).first()

    if group:
        group_info = {
            "starosta": group.starosta,
            "contact_starosta": group.contact_starosta
        }
        return jsonify(group_info), 200
    else:
        return jsonify({"error": "Group not found"}), 404


@app.route("/group-list", methods=["GET"])
def get_group_list():
    """
    Get a list of all academic groups.
    """
    groups = Groups.query.all()
    group_list = [{"group_name": group.group_name} for group in groups]
    return jsonify(group_list), 200


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
