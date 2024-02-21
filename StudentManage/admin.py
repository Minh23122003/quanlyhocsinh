from StudentManage.models import *
from StudentManage import app, db, dao, utils
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request,render_template

admin = Admin(app=app, name='Quản lý học sinh', template_mode='bootstrap4')


class AuthenticatedAdmin(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class Authenticated_Admin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class StatsView(AuthenticatedAdmin):
    @expose("/")
    def index(self):

        return self.render('admin/Statistics.html', subjects=dao.get_subject(), semesters=dao.get_semester())

class ChangeRule(AuthenticatedAdmin):
    @expose("/")
    def index(self):

        return self.render('admin/ChangeRule.html', quantity=app.config['soluong'],
                           min_age=app.config['mintuoi'], max_age=app.config['maxtuoi'])


class MySubjectView(Authenticated_Admin):
    column_list=['id_subject', 'name_subject']
    column_searchable_list = ['name_subject']
    column_filters = ['id_subject', 'name_subject']
    column_editable_list = ['name_subject']
    edit_modal = True


class MyClassView(Authenticated_Admin):
    column_list=['id_class', 'name_class']
    column_searchable_list = ['name_class']
    column_filters = ['id_class', 'name_class']
    column_editable_list = ['name_class']
    edit_modal = True


class MyUserView(Authenticated_Admin):
    # column_list=['id', 'name_class']
    # column_searchable_list = ['name_class']
    # column_filters = ['id_class', 'name_class']
    column_editable_list = ['name']
    edit_modal = True


class MyTeacherView(Authenticated_Admin):
    column_list=['id_teacher', 'name_teacher']
    column_searchable_list = ['name_teacher']
    column_filters = ['id_teacher', 'name_teacher']
    column_editable_list = ['name_teacher']
    edit_modal = True


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(MyUserView(User, db.session))
admin.add_view(MyTeacherView(Teacher, db.session))
admin.add_view(MySubjectView(Subject, db.session))
admin.add_view(MyClassView(Class, db.session))
admin.add_view(StatsView(name='Thống kê báo cáo'))
admin.add_view(ChangeRule(name='Thay đổi quy định'))
admin.add_view(LogoutView(name='Đăng xuất'))


