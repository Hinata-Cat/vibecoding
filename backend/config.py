import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGO_DB') or 'virtual_tourism',
        'host': os.environ.get('MONGO_HOST') or 'localhost',
        'port': int(os.environ.get('MONGO_PORT') or 27017),
        'username': os.environ.get('MONGO_USER') or None,
        'password': os.environ.get('MONGO_PASSWORD') or None
    }
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size