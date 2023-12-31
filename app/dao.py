from app.models import User, UserRoleEnum
from app import app, db
import hashlib
from flask_login import current_user

def get_user_by_id(user_id):
    return User.query.get(user_id)


def auth_admin(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password), User.user_role.__eq__(UserRoleEnum.ADMIN)).first()