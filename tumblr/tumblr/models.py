from enum import unique
import enum
from os import name, stat_result
from flask import Flask, render_template, redirect, request, session,make_response, flash,jsonify
from flask.helpers import safe_join
#from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, current
from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, UserMixin, logout_user,current_user
from passlib.hash import sha256_crypt
from sqlalchemy import join

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tumblr.sqlite3'
app.config["SESSION_PERMANENT"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "thisisddsecret"
#Session(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

class POST_TYPE(enum.Enum):
    IMAGE='Image'
    AUDIO='Audio'
    VIDEO='Video'
    TEXT='Text'
    GIF='Gif'
    
    
class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False,unique=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    #----------default none values -------------------------------
    user_image = db.Column(db.String(255), nullable=False,default=None)
    website_url = db.Column(db.String(255), nullable=False,default=None)
    facebook = db.Column(db.String(255), nullable=False,default=None)
    twitter = db.Column(db.String(255), nullable=False,default=None)
    instagram = db.Column(db.String(255), nullable=False,default=None)
    linkedin =db.Column(db.String(255), nullable=False,default=None)
    
    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model): #Question
    __tablename__ = 'Post'
    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(255), nullable=False)
    post_description = db.Column(db.String(255), nullable=False)
    post_category = db.Column(db.String(255), nullable=False)
    post_type= db.Column(db.Enum(POST_TYPE), nullable=False)
    post_datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Post', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.post_title

class Comment(db.Model):
    __tablename__ = 'Comment'
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(255), nullable=False)
    comment_datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    post_id = db.Column(db.Integer, db.ForeignKey('Post.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    
    # person_id = db.Column(db.Integer, db.ForeignKey('Person.person_id'), nullable=False)
    post = db.relationship('Post', backref=db.backref('comment', lazy=True))
    user = db.relationship('User', backref=db.backref('comment', lazy=True)) 

    def __repr__(self):
        return '<Comment %r>' % self.comment_text

class Like(db.Model):
    __tablename__ = 'Like'
    like_id = db.Column(db.Integer, primary_key=True)
    like_post=db.Column(db.String(255), nullable=False,default=None)
  
    post_id = db.Column(db.Integer, db.ForeignKey('Post.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)

    post = db.relationship('Post', backref=db.backref('comment', lazy=True))
    user = db.relationship('User', backref=db.backref('comment', lazy=True)) 

    def __repr__(self):
        return '<Like %r>' % self.like_id