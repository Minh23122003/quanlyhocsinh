from StudentManage.models import *
from StudentManage import app
import hashlib
from sqlalchemy import func
from flask import jsonify


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_class():
    return Class.query.all()


def get_class_by_id_grade(id_grade):
    return Class.query.filter(Class.id_grade.__eq__(id_grade)).all()


def get_class_by_id(id_class):
    return Class.query.filter(Class.id_class.__eq__(id_class)).first()


def get_class_is_blank():
    classes = Class.query.all()
    classes_blank = []
    for c in classes:
        if len(c.students) < app.config['soluong']:
            classes_blank.append(c)
    return classes_blank


def get_student_by_class(id_class):
    return Student.query.filter(Student.id_class.__eq__(id_class)).all()


def get_student():
    return Student.query.all()


def get_student_by_name(name):
    return Student.query.filter(Student.name.contains(name.lower())).all()


def get_student_by_id(id):
    return Student.query.get(id)


def get_student_by_id_grade(id_grade):
    return Student.query.filter(Student.id_grade == id_grade).all()


def get_subject():
    return Subject.query.all()


def get_subject_by_id(id):
    return Subject.query.filter(Subject.id_subject == id).first()


def get_semester():
    return Semester.query.all()


def get_semester_by_id(id):
    return Semester.query.filter(Semester.id_semester == id).first()


def get_grade():
    return Grade.query.all()


def calc_semester_score_average(id_class, id_semester):
    student = get_student_by_class(id_class)
    subjects = get_subject()

    scores = {}

    for i in range(len(student)):
        scores[i] = {
            'id_student': student[i].id,
            'score': 0,
        }

    for subject in subjects:
        test_15m = db.session.query(Test.id_student, func.sum(Test.score), func.count(Test.score)) \
            .join(Student, Student.id == Test.id_student) \
            .filter(Test.id_semester == id_semester, Test.id_subject == subject.id_subject,
                    Student.id_class == id_class, Test.type == '15 phút') \
            .group_by(Test.id_student).all()

        test_45m = db.session.query(Test.id_student, func.sum(Test.score), func.count(Test.score)) \
            .join(Student, Student.id == Test.id_student) \
            .filter(Test.id_semester == id_semester, Test.id_subject == subject.id_subject,
                    Student.id_class == id_class, Test.type == '1 tiết') \
            .group_by(Test.id_student).all()

        test_final = db.session.query(Test.id_student, func.sum(Test.score), func.count(Test.score)) \
            .join(Student, Student.id == Test.id_student) \
            .filter(Test.id_semester == id_semester, Test.id_subject == subject.id_subject,
                    Student.id_class == id_class, Test.type == 'Cuối kỳ') \
            .group_by(Test.id_student).all()

        if test_15m and test_45m and test_final:
            for i in range(len(test_15m)):
                a = float(test_15m[i][1])
                b = float(test_45m[i][1])
                c = float(test_final[i][1])
                x = int(test_15m[i][2])
                y = int(test_45m[i][2])
                z = int(test_final[i][2])
                scores[i]['score'] =scores[i]['score'] + round((a + b * 2 + c * 3)/(x + y * 2 +z * 3),1)
    for i in range(len(scores)):
        if scores[i]['score'] != 0:
            scores[i]['score'] = round(scores[i]['score'] / len(subjects), 1)
    return scores


def statistics_subject(id_class, id_subject, id_semester):
    student = get_student_by_class(id_class)
    scores = {}

    for i in range(len(student)):
        scores[i] = {
            'id_student': student[i].id,
            'score': 0,
        }
    test_15m = db.session.query(Test.id_student, func.sum(Test.score), func.count(Test.score)) \
        .join(Student, Student.id == Test.id_student) \
        .filter(Test.id_semester == id_semester, Test.id_subject == id_subject,
                Student.id_class == id_class, Test.type == '15 phút') \
        .group_by(Test.id_student).all()

    test_45m = db.session.query(Test.id_student, func.sum(Test.score), func.count(Test.score)) \
        .join(Student, Student.id == Test.id_student) \
        .filter(Test.id_semester == id_semester, Test.id_subject == id_subject,
                Student.id_class == id_class, Test.type == '1 tiết') \
        .group_by(Test.id_student).all()

    test_final = db.session.query(Test.id_student, func.sum(Test.score), func.count(Test.score)) \
        .join(Student, Student.id == Test.id_student) \
        .filter(Test.id_semester == id_semester, Test.id_subject == id_subject,
                Student.id_class == id_class, Test.type == 'Cuối kỳ') \
        .group_by(Test.id_student).all()
    if test_15m and test_45m and test_final:
        for i in range(len(test_15m)):
            a = float(test_15m[i][1])
            b = float(test_45m[i][1])
            c = float(test_final[i][1])
            x = int(test_15m[i][2])
            y = int(test_45m[i][2])
            z = int(test_final[i][2])
            scores[i]['score'] = round((a + b * 2 + c * 3) / (x + y * 2 + z * 3), 1)
    return scores

def create_class_list():
    grade = get_grade()
    for g in grade:
        students = get_student_by_id_grade(g.id_grade)
        classes = get_class_by_id_grade(g.id_grade)
        i = 0
        for s in students:
            if s.id_class:
                continue
            else:
                s.id_class = classes[i].id_class
                db.session.commit()
                i = i + 1
            if i == len(classes):
                i = 0
    return get_student()


def auth_admin(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password), User.user_role.__eq__(UserRoleEnum.ADMIN)).first()


def auth_staff(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password), User.user_role.__eq__(UserRoleEnum.STAFF)).first()


def auth_teacher(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password), User.user_role.__eq__(UserRoleEnum.TEACHER)).first()


if __name__ == '__main__':
    with app.app_context():
        print(statistics_subject(1,1,1))
