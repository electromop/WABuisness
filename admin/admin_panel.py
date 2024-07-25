from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from database.models import Base, User, UserMaterials, Material, Question, Keyword
from database.db_reader import db_config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = db_config.database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#class UserMaterialsView(ModelView):
#    column_list = ('user_id', 'material_id', 'count')
#    form_columns = ('user_id', 'material_id', 'count')


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not self._is_accessible():
            return redirect(url_for('login'))
        return super(MyAdminIndexView, self).index()

    def _is_accessible(self):
        # Простая проверка на примере
        return request.args.get('username') == 'admin' and request.args.get('password') == 'admin'


admin = Admin(app, name='Панель', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserMaterials, db.session))
admin.add_view(ModelView(Material, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(Keyword, db.session))


#@app.route('/')
#def home():
#    return redirect("/admin")


@app.route('/login')
def login():
    return '''
        <form action="/admin" method="get">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <input type="submit" value="Login">
        </form>
    '''


if __name__ == '__main__':
    with app.app_context():
        Base.metadata.create_all(bind=db.engine)
    app.run(debug=False, host="0.0.0.0", port=5000)
