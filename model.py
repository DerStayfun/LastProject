import sqla_wrapper
import os

#SQLITE_File = ":memory:"
SQLITE_File = "localhost.sqlite"

db = sqla_wrapper.SQLAlchemy(os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_File}"))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique = True, nullable=False)
    email = db.Column(db.String, unique = True, nullable=False)
    password = db.Column(db.String, nullable=False)
    session_token = db.Column(db.String, nullable=True)
    session_expiry_datetime = db.Column(db.DateTime, nullable=True)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String, unique=True)
    taste = db.Column(db.String)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    author = db.Column(db.String)
    genre = db.Column(db.String)