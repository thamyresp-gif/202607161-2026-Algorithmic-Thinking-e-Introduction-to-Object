import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "orcamento-r-m-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///orcamento.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONCURRENT_USERS = 10