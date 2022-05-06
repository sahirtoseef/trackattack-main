import os

class Config:
    SECRET_KEY = "4eae2cf92679a7bb7472236234cd456a3e18a4c17cc5f6c2bcf9986bd30fdcbb"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASS')
    PAGINATION_PER_PAGE = 10