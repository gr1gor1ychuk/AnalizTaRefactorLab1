def order_lessons(lessons):
    day_order = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5}
    return sorted(lessons, key=lambda lesson: (day_order.get(lesson.day, 99), lesson.class_order))


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
