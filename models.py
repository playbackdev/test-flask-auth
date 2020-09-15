from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(32), index = True, unique = True)
    password = db.Column(db.String(64))
    fio = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r>' % (self.login)
		
    def set_password(self, pswd):
        self.password = generate_password_hash(pswd)

    def check_password(self,  pswd):
        return check_password_hash(self.password, pswd)