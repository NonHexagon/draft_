import random
import sqlite3
from sqlalchemy import Sequence, create_engine
from databaseCreator import Users, File, Session, Base
from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
@app.route('/home')
def index():
    user_list = Base.query.order_by
    return render_template('index.html', user_list=user_list)


@app.route('/register', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        user_name = request.form['user_name']
        print(user_name)
        f_name = request.form['f_name']
        print(f_name)
        l_name = request.form['l_name']
        print(l_name)
        email = request.form['email']
        print(email)
        tmp_passwd = 'weytr732d'
        new_user = Users(user_name=user_name, f_name=f_name, l_name=l_name, email=email, tmp_passwd=tmp_passwd)
        try:
            session_db = Session()
            session_db.add(new_user)
            session_db.commit()
            print(f'Был добавлен новый пользователь: {l_name} {f_name} с ником {user_name}')
        except AttributeError:
            return 'Что-то пошло не так!'
        return redirect('/')

    elif request.method == 'GET':
        return render_template('register_form.html')


if __name__ == "__main__":
    app.run(debug=True)
