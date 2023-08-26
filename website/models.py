from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import ForeignKeyConstraint, sql


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    attachment = db.Column(db.LargeBinary)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer)
    solved = db.Column(db.Boolean)
    post_level = db.Column(db.String)

    user = db.relationship('User', backref='posts')

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id', 'post_level'],
            ['user.id', 'user.education_level']
        ),
    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    post = db.relationship('Post')
    education_level = db.Column(db.String(150))
    school = db.Column(db.String(150))
    role = db.Column(db.String(50))

class Mentor(User):
    csp = db.Column(db.String(10))
    code = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    # answer = db.relationship('Answer')
    
# class Answer(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     answer = db.Column(db.String(150))
#     answer_attachment = db.Column(db.LargeBinary)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


    


