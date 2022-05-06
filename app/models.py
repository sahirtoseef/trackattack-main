from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    full_name = db.Column(db.String(60))
    age = db.Column(db.Integer)

    entries = db.relationship('Entry', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    visited_date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    age = db.Column(db.Integer)
    last_visited_location = db.Column(db.String(100))
    last_visited_location_lat = db.Column(db.String(100))
    last_visited_location_long = db.Column(db.String(100))
    covid_status = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.full_name}', '{self.last_visited_location}')"