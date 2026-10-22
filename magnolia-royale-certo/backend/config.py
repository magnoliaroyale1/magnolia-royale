import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True, 'isolation_level': 'READ COMMITTED'}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('COOKIE_SECURE') == '1'
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024
    UPLOAD_DIR = BASE_DIR / 'uploads'
    MAILBOX_DIR = BASE_DIR / 'mailbox'
    DEMO_MODE = os.environ.get('DEMO_MODE', '1') == '1'
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://127.0.0.1:5173')
