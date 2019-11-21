import sqla_wrapper
import os


db = sqla_wrapper.SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique = True)
    email = db.Column(db.String, unique = True)


class Recipe:
    def __init__(self, name, taste, description):
        self.name = name
        self.taste = taste
        self.description = description