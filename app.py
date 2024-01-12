"""Blogly application."""

from flask import Flask
from user_routes import users_bp
from blogpost_routes import blogposts_bp
from tag_routes import tags_bp
from models import db, connect_db

app = Flask(__name__)

app.register_blueprint(users_bp)
app.register_blueprint(blogposts_bp)
app.register_blueprint(tags_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"


