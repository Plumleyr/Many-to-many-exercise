"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ USER """

    __tablename__ = "user"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(),
                            nullable = False)
    last_name = db.Column(db.String(),
                            nullable = False)
    image_url = db.Column(db.String(),
                            nullable = False)

class Blogpost(db.Model):
    """ POST """

    __tablename__ = "post"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    title = db.Column(db.Text,
                        nullable = False,
                        unique = True)
    content = db.Column(db.Text,
                        nullable = False)
    created_at = db.Column(db.DateTime,
                            nullable = False,
                            default = datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'))

    user = db.relationship('User', 
                            backref='blogposts')