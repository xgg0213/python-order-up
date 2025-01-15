import os


class Configuration:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"  # SQLite database file
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Optional, disables event tracking