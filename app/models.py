from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
from datetime import datetime
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
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.STAFF)

    def __str__(self):
        self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # u1 = User(name='Admin', username='admin',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.ADMIN)
        # u2 = User(name='Staff', username='staff',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.STAFF)
        # u3 = User(name='Teacher', username='teacher',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.TEACHER)
        # db.session.add_all([u1, u2, u3])
        # db.session.commit()
