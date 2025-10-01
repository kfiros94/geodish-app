import os

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/geodish')
    SECRET_KEY = os.getenv('SECRET_KEY', 'geodish-secret-key-2024')
