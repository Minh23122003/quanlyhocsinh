from flask import render_template, request, redirect, session, jsonify
from StudentManage import app, login, db, utils
from StudentManage.models import *
import dao
from flask_login import login_user, current_user, logout_user
from StudentManage import admin
import string
from datetime import datetime


@app.route("/")
def index():
    return render_template('layout/base.html')


@app.route('/admin/login', methods=['post'])
def login_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    admin = dao.auth_admin(username=username, password=password)
    if admin:
        login_user(admin)

    return redirect('/admin')


@app.route('/login', methods=['get', 'post'])
def login_view():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        staff = dao.auth_staff(username=username, password=password)
        if staff:
            login_user(staff)
            return render_template('staff.html')
        else:
            err_msg = 'Tên đăng nhập hoặc mật khẩu không chính xác. Vui lòng thử lại!'

        teacher = dao.auth_teacher(username=username, password=password)
        if teacher:
            err_msg = ''
            login_user(teacher)
            return render_template('teacher.html')
    return render_template('login.html', err_msg=err_msg)


@app.route('/logout')
def logout_view():
    logout_user()
    return redirect('/login')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/InputScores")
def InputScores():
    return render_template('InputScores.html', classes=dao.get_class(), subjects=dao.get_subject(), semesters=dao.get_semester())


@app.route("/OutputScores")
def OutputScores():
    return render_template('OutputScores.html', classes=dao.get_class(), semesters=dao.get_semester())


@app.route("/AddStudent")
def AddStudent():
    return render_template('AddStudent.html')


@app.route("/CreateClassList")
def CreateClassList():
    student = dao.create_class_list()
    classes = dao.get_class()

    return render_template('CreateClassList.html', classes=classes)


@app.route("/AdjustClass")
def AdjustClass():
    return render_template('AdjustClass.html', classes=dao.get_class_is_blank())


@app.route("/ThemHocSinh", methods=['POST'])
def ThemHocSinh():
    err_msg = ''
    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        sex = request.form.get('sex')
        DoB = request.form.get('DoB')
        address = str(request.form.get('address'))
        phonenumber = request.form.get('phonenumber')
        email = request.form.get('email')
        grade = request.form.get('grade')
        substring = email[(len(email) - 10):]
        if len(phonenumber) != 10:
            err_msg = 'Số điện thoại sai. Vui lòng nhập lại!'
            return render_template('AddStudent.html', err_msg=err_msg)
        if not substring.__eq__('@gmail.com'):
            err_msg = 'Email sai. Vui lòng nhập lại!'
            return render_template('AddStudent.html', err_msg=err_msg)
        try:
            birthdate = datetime.strptime(DoB, '%Y-%m-%d')
        except:
            err_msg = 'Bạn chưa nhập ngày sinh. Vui lòng thử lại!'
            return render_template('AddStudent.html', err_msg=err_msg)
        if (app.config['nambatdau'] - birthdate.year) < app.config['mintuoi'] or (
                app.config['nambatdau'] - birthdate.year) > app.config['maxtuoi']:
            err_msg = 'Ngày sinh không hợp lệ. Vui lòng thử lại!'
            return render_template('AddStudent.html', err_msg=err_msg)

        student = Student(name=fullname, sex=sex, DoB=DoB, address=address, phonenumber=phonenumber,
                            email=email, id_grade=grade)
        db.session.add(student)
        db.session.commit()
        err_msg = 'Lưu thành công'
        return render_template('AddStudent.html', err_msg=err_msg)


@app.route("/api/searchStudent", methods=['POST'])
def SearchStudent():
    if request.method.__eq__('POST'):
        name = request.json.get('searchstudent')
        students = dao.get_student_by_name(name)
        stu = {}
        stu[0] = {"quantity" : len(students)}

        for i in range(1,len(students)+1):
            if students[i-1].id_class:
                stu[i] = {
                    "id": students[i-1].id,
                    "name": students[i-1].name,
                    "class": students[i-1].Class.name_class
                }
            else: stu[i] = {
                    "id": students[i-1].id,
                    "name": students[i-1].name,
                    "class": "Chưa có lớp"
                }

        return stu

@app.route('/api/changeClass', methods=['post'])
def ChangeClass():
    id_student = request.json.get('id_student')
    id_class = request.json.get('id_class')
    student = dao.get_student_by_id(id_student)
    Class = dao.get_class_by_id(id_class)
    blank_class = dao.get_class_is_blank()

    if not student:
        return jsonify({'content': 'ID học sinh không tồn tại. Vui lòng kiểm tra lại'})

    if not Class:
        return jsonify({'content': 'ID lớp học không tồn tại. Vui lòng kiểm tra lại'})

    if not Class in blank_class:
        return jsonify({'content': 'Lớp học đã đầy. Vui lòng chọn lớp khác'})

    if student.id_grade == Class.id_grade:
        student.id_class = Class.id_class
        db.session.commit()
        return jsonify({'content': 'Thành công'})
    else:
        return jsonify({'content': 'Lớp chuyển đến không thuộc khối của học sinh'})


@app.route('/api/printClass', methods=['post'])
def PrintClass():
    id_class = request.json.get('id_class')
    classes = dao.get_class_by_id(id_class)
    students = dao.get_student_by_class(id_class)
    stu = {}

    stu[0] = {
        "id": classes.id_class,
        "class": classes.name_class,
        "quantity": len(students)
    }

    for i in range(1, len(students) + 1):
        stu[i] = {
            "name": students[i-1].name,
            "sex": students[i-1].sex,
            "DoB": students[i-1].DoB.strftime("%d/%m/%Y"),
            "address": students[i-1].address
        }

    return stu


@app.route('/api/searchClass', methods=['post'])
def SearchClass():
    id_class = request.json.get('searchclass')
    students = dao.get_student_by_class(id_class)
    stu = {}

    stu[0] = {
        "name_class": students[0].Class.name_class,
        "num_row_15m": request.json.get('num_row_15m'),
        "num_row_45m": request.json.get('num_row_45m'),
        "quantity": len(students)
    }

    for i in range(1,len(students) + 1):
        stu[i] = {
            "id": students[i-1].id,
            "name": students[i-1].name
        }

    session['num_test'] = {"num_row_15m": request.json.get('num_row_15m'),
                           "num_row_45m": request.json.get('num_row_45m'), "id_class": id_class}

    return stu


@app.route('/api/saveScores', methods=['post'])
def SaveScores():
    stu = request.json.get('scores')
    id_subject = request.json.get('id_subject')
    id_semester = request.json.get('id_semester')
    num_row_15m = len(session['num_test']['num_row_15m'])
    num_row_45m = len(session['num_test']['num_row_45m'])
    student = dao.get_student_by_class(session['num_test']['id_class'])

    for i in range(len(stu)):
        for j in range(num_row_15m + num_row_45m + 1):
            if not stu[i][j]:
                return jsonify({'content': 'Có học sinh chưa nhập điểm. Vui lòng kiểm tra lại!'})
            elif float(stu[i][j]) > 10 or float(stu[i][j]) < 0:
                return jsonify({'content': 'Điểm không hợp lệ. Vui lòng kiểm tra lại!'})

    for s in student:
        tests = Test.query.filter(Test.id_student==s.id, Test.id_subject==id_subject, Test.id_semester==id_semester).all()
        for t in tests:
            db.session.delete(t)
            db.session.commit()

    for i in range(len(stu)):
        for j in range(num_row_15m + num_row_45m + 1):
            type = ''
            if j < num_row_15m:
                type = '15 phút'
            elif j < (num_row_15m + num_row_45m):
                type = '1 tiết'
            else:
                type = 'Cuối kỳ'
            test = Test(type=type, score=round(float(stu[i][j]),1), id_student=student[i].id,
                        id_subject=id_subject, id_semester=id_semester)
            db.session.add(test)
            db.session.commit()


    return jsonify({'content': 'Lưu thành công'})


@app.route('/api/printScores', methods=['post'])
def PrintScores():
    id_class = request.json.get('id_class')
    id_semester = request.json.get('id_semester')
    semester_1 = dao.calc_semester_score_average(id_class=id_class, id_semester=id_semester)
    semester_2 = dao.calc_semester_score_average(id_class=id_class, id_semester=int(id_semester)+1)
    schoolyear = ''
    if id_semester == '1':
        schoolyear = 'Năm học 2020-2021'
    elif id_semester == '3':
        schoolyear = 'Năm học 2021-2022'
    elif id_semester == '5':
        schoolyear = 'Năm học 2022-2023'
    elif id_semester == '7':
        schoolyear = 'Năm học 2023-2024'
    result = {}
    result[0] = {
        'quantity': len(semester_1),
        'class': dao.get_class_by_id(id_class).name_class,
        'schoolyear': schoolyear
    }
    for i in range(len(semester_1)):
        result[i+1] = {
            'name_student': dao.get_student_by_id(semester_1[i]['id_student']).name,
            'semester_1': semester_1[i]['score'],
            'semester_2': semester_2[i]['score']
        }

    return result


@app.route("/api/statisticsScore", methods=['POST'])
def StatisticsScore():
    id_subject = request.json.get('id_subject')
    id_semester = request.json.get('id_semester')
    classes = dao.get_class()
    semester = 0
    schoolyear = ''
    if int(id_semester) % 2 == 0:
        semester = 2
    else:
        semester = 1
    if id_semester == '1':
        schoolyear = 'Năm học 2020-2021'
    elif id_semester == '3':
        schoolyear = 'Năm học 2021-2022'
    elif id_semester == '5':
        schoolyear = 'Năm học 2022-2023'
    elif id_semester == '7':
        schoolyear = 'Năm học 2023-2024'
    stu = {}
    stu[0] = {
        'subject': dao.get_subject_by_id(id_subject).name_subject,
        'semester': semester,
        'schoolyear': schoolyear,
        'quantity': len(classes)
    }
    for i in range(len(classes)):
        statistics = dao.statistics_subject(id_class=classes[i].id_class, id_subject=id_subject, id_semester=id_semester)
        count = 0
        for j in range(len(statistics)):
            if statistics[j]['score'] >= 5:
                count = count + 1
        rate = 0
        if len(statistics) == 0:
            rate = 0
        else:
            rate = round(float(count / len(statistics) * 100), 1)
        stu[i+1]= {
            'class': classes[i].name_class,
            'quantity_student': len(statistics),
            'quantity_passed': count,
            'rate': rate
        }
    return stu


@app.route("/api/changeRule", methods=['POST'])
def ChangeRule():
    quantity = int(request.json.get('quantity'))
    min_age = int(request.json.get('min_age'))
    max_age = int(request.json.get('max_age'))

    if quantity <= 0 or min_age <= 0 or max_age <= 0:
        return jsonify({'status': 200, 'content': 'Thông tin không hợp lệ. Vui lòng kiểm tra lại!'})
    if min_age >= max_age:
        return jsonify({'status': 200, 'content': 'Tuổi lớn nhất phải lớn hơn tuổi nhỏ nhất. Vui lòng kiểm tra lại!'})
    classes = dao.get_class()
    max = 0
    for c in classes:
        student = dao.get_student_by_class(c.id_class)
        if max < len(student):
            max = len(student)
    if quantity < max:
        return jsonify({'status': 200, 'content': str.format('Sĩ số tối đa phải lớn hơn {0}. Vui lòng kiểm tra lại!', max)})
    app.config['soluong'] = quantity
    app.config['mintuoi'] = min_age
    app.config['maxtuoi'] = max_age
    return jsonify({'status': 500, 'content': 'Thành công!'})


if __name__ == '__main__':
    app.run(debug=True)