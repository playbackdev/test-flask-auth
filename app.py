from flask import Flask, request, jsonify, render_template, redirect
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user
import sqlite3
import json
import os
import re

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'my_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_MIGRATE_REPO'] = SQLALCHEMY_MIGRATE_REPO
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from models import User


@app.route('/',methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect("http://yandex.ru", code=302)
    return render_template('index.html')
	

@app.route('/reg',methods=['POST'])
def reg():
    data = request.get_json()
    if data['f'] and data['l'] and data['p']:
        if not re.fullmatch(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+', data['f']):
            return jsonify({'status':1,'message':'Введите ФИО в формате "Фамилия Имя Отчество"'})
        if len(data['p']) < 6:
            return jsonify({'status':2,'message':'Пароль должен быть хотя бы 6 символов'})
        dbUser = User.query.filter_by(login=data['l']).first()
        if dbUser is None:
            newUser = User(login=data['l'], password=data['p'], fio=data['f'])
            newUser.set_password(data['p'])
            db.session.add(newUser)
            db.session.commit()
            print(newUser.id)
            return jsonify({'status':0,'message':'Регистрация прошла успешно'})
        else:
            return jsonify({'status':3,'message':'Такой пользователь уже существует'})
    else:
        return jsonify({'status':4,'message':'ФИО, логин и пароль не должны быть пустыми'})
		
@app.route('/pre_signin',methods=['POST'])
def pre_signin():
    data = request.get_json()
    if(data['l'] and data['p']):
        dbUser = User.query.filter_by(login=data['l']).first()
        if not (dbUser is None):
            if dbUser.check_password(data['p']):
                login_user(dbUser, remember=True)
                return jsonify({'status':0,'message':'Авторизация прошла успешно'})
            else:
                return jsonify({'status':1,'message':'Неверный логин или пароль'})
        else:
            return jsonify({'status':2,'message':'Неверный логин или пароль'})
    else:
        return jsonify({'status':3,'message':'Введите логин и пароль'})
	
@app.route('/signin',methods=['POST'])
def signin():
    #если кука есть - то редирект
    print(request.data)
    return redirect("http://yandex.ru", code=302)