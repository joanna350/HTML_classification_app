import os

class Config(object):
    secret_key = "secret key"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    cwd = os.getcwd() + '/uploads'
    if not os.path.isdir(cwd):
        os.mkdir(cwd)

    UPLOAD_FOLDER = cwd

class ProductionConfig(Config):
    DEBUG = False