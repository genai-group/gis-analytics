import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///your-database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add other configuration settings as needed
