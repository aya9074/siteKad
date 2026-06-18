import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Базовые настройки приложения"""
    
    # Секретный ключ (из .env)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # База данных (из .env)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///data/site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Режим отладки (из .env)
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Загрузка файлов
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 МБ
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Администратор (из .env)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    
    # Настройки для форм
    WTF_CSRF_ENABLED = True
