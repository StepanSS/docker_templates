import os
from dotenv import load_dotenv


# By default, load_dotenv doesn't override existing environment variables.
load_dotenv('.flaskenv')


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///sqlite.db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite.db" # use sqlite
    SQLALCHEMY_TRACK_MODIFICATIONS = False