from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from StudentManage import db, app
from flask_login import UserMixin
import enum
import hashlib


class UserRoleEnum(enum.Enum):
    ADMIN = 1
    STAFF = 2
    TEACHER = 3


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRoleEnum), nullable=False)

    def __str__(self):
        self.name


class Grade(db.Model):
    __tablename__ = 'Grade'
    id_grade = Column(Integer, primary_key=True, autoincrement=True)
    name_grade = Column(Enum('Grade 10', 'Grade 11', 'Grade 12'), nullable=False)
    classes = relationship('Class', backref='grade', lazy=True)
    students = relationship('Student', backref='Grade', lazy=True)


class Class(db.Model):
    __tablename__ = 'Class'
    id_class = Column(Integer, primary_key=True, autoincrement=True)
    name_class = Column(String(50), nullable=False)
    id_grade = Column(Integer, ForeignKey(Grade.id_grade), nullable=False)
    students = relationship('Student', backref='Class', lazy=True)


class Semester(db.Model):
    __tablename__ = 'Semester'
    id_semester = Column(Integer, primary_key=True, autoincrement=True)
    name_semester = Column(String(50), nullable=False)
    tests = relationship('Test', backref='Semester', lazy=True)


class Student(db.Model):
    __tablename__ = 'Student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    sex = Column(Enum('Nam', 'Nữ'), nullable=False)
    DoB = Column(DateTime, nullable=False)
    address = Column(String(100), nullable=False)
    phonenumber = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    id_class = Column(Integer, ForeignKey(Class.id_class), nullable=True)
    id_grade = Column(Integer, ForeignKey(Grade.id_grade), nullable=False)
    tests = relationship('Test', backref='Student', lazy=True)


class Subject(db.Model):
    __tablename__ = 'Subject'
    id_subject = Column(Integer, primary_key=True, autoincrement=True)
    name_subject = Column(String(100), nullable=False)
    tests = relationship('Test', backref='Subject', lazy=True)
    teachers = relationship('Teacher', backref='Subject', lazy=True)


class Teacher(db.Model):
    __tablename__ = 'Teacher'
    id_teacher = Column(Integer, primary_key=True, autoincrement=True)
    name_teacher = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable= True)
    id_user = Column(Integer, ForeignKey(User.id), nullable= True)
    id_subject = Column(Integer, ForeignKey(Subject.id_subject), nullable= False)


class Test(db.Model):
    __tablename__ = 'Test'
    id_test = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum('15 phút', '1 tiết', 'Cuối kỳ'), nullable=False)
    score = Column(Float, nullable=False)
    id_student = Column(Integer, ForeignKey(Student.id), nullable=False)
    id_subject = Column(Integer, ForeignKey(Subject.id_subject), nullable=False)
    id_semester = Column(Integer, ForeignKey(Semester.id_semester), nullable=False)


class_teacher = db.Table('class_teacher',
                            Column('id_class', Integer, ForeignKey(Student.id), primary_key=True),
                            Column('id_teacher', Integer, ForeignKey(Teacher.id_teacher), primary_key=True))

student_subject = db.Table('student_subject',
                           Column('id_student', Integer, ForeignKey(Student.id), primary_key=True),
                           Column('id_subject', Integer, ForeignKey(Subject.id_subject), primary_key=True))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        u1 = User(name='Admin', username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.ADMIN)
        u2 = User(name='Staff', username='staff',
                  password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.STAFF)
        u3 = User(name='Teacher', username='teacher',
                  password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.TEACHER)
        db.session.add_all([u1, u2, u3])
        db.session.commit()

        grade1=Grade(name_grade='Grade 10')
        grade2 = Grade(name_grade='Grade 11')
        grade3 = Grade(name_grade='Grade 12')
        db.session.add_all([grade1, grade2, grade3])
        db.session.commit()

        c1=Class(name_class='10A1', id_grade=1)
        c2 = Class(name_class='10A2', id_grade=1)
        c3 = Class(name_class='10A3', id_grade=1)
        c4 = Class(name_class='10A4', id_grade=1)
        c5 = Class(name_class='10A5', id_grade=1)
        c6 = Class(name_class='11A1', id_grade=2)
        c7 = Class(name_class='11A2', id_grade=2)
        c8 = Class(name_class='11A3', id_grade=2)
        c9 = Class(name_class='11A4', id_grade=2)
        c10 = Class(name_class='11A5', id_grade=2)
        c11 = Class(name_class='12A1', id_grade=3)
        c12 = Class(name_class='12A2', id_grade=3)
        c13 = Class(name_class='12A3', id_grade=3)
        c14 = Class(name_class='12A4', id_grade=3)
        c15 = Class(name_class='12A5', id_grade=3)
        db.session.add_all([c1, c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15])
        db.session.commit()

        s1 = Subject(name_subject="Ngữ văn")
        s2 = Subject(name_subject="Toán")
        s3 = Subject(name_subject="Ngoại ngữ")
        s4 = Subject(name_subject="Vật lý")
        s5 = Subject(name_subject="Hóa học")
        s6 = Subject(name_subject="Sinh học")
        s7 = Subject(name_subject="Lịch sử")
        s8 = Subject(name_subject="Địa lý")
        s9 = Subject(name_subject="Giáo dục công dân")
        s10 = Subject(name_subject="Tin học")
        s11 = Subject(name_subject="Giáo dục quốc phòng và an ninh")
        s12 = Subject(name_subject="Công nghệ")
        db.session.add_all([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12])
        db.session.commit()

        s1 = Semester(name_semester="Học kỳ 1 năm học 2020-2021")
        s2 = Semester(name_semester="Học kỳ 2 năm học 2020-2021")
        s3 = Semester(name_semester="Học kỳ 1 năm học 2021-2022")
        s4 = Semester(name_semester="Học kỳ 2 năm học 2021-2022")
        s5 = Semester(name_semester="Học kỳ 1 năm học 2022-2023")
        s6 = Semester(name_semester="Học kỳ 2 năm học 2022-2023")
        s7 = Semester(name_semester="Học kỳ 1 năm học 2023-2024")
        s8 = Semester(name_semester="Học kỳ 2 năm học 2023-2024")
        db.session.add_all([s1, s2,s3,s4,s5,s6,s7,s8])
        db.session.commit()
