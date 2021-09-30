import os
class Config:
    SECRET_KEY="thisissecretkey"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:1234@localhost/library'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    DEBUG=False

class DevConfig(Config):
    DEBUG = True
    SECRET_KEY="thisissecretkey"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:1234@localhost/library'


config_options = {
'development':DevConfig,
'production':ProdConfig
}