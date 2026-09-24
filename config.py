import os
import tempfile
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # SECRET_KEY resolution: In production (Vercel / FLASK_ENV=production), SECRET_KEY MUST be provided via environment.
    _env_secret = os.environ.get('SECRET_KEY')
    _is_prod = bool(os.environ.get('VERCEL') or os.environ.get('FLASK_ENV') == 'production')

    if _is_prod:
        if not _env_secret:
            raise RuntimeError("CRITICAL SECURITY ERROR: SECRET_KEY environment variable is required in production / Vercel deployment.")
        SECRET_KEY = _env_secret
    else:
        SECRET_KEY = _env_secret or 'dev-only-local-secret-key-do-not-use-in-production'
    
    # Session Cookie Security Configuration for Production HTTPS & Serverless (Vercel)
    SESSION_COOKIE_NAME = 'jcc_admin_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True if _is_prod else False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Database URL handling
    raw_db_uri = os.environ.get('DATABASE_URL') or os.environ.get('DATABASE_URI') or os.environ.get('POSTGRES_URL')
    
    if raw_db_uri:
        # Normalize cloud PostgreSQL prefix
        prefix = 'postgres:'
        if raw_db_uri.startswith(prefix):
            raw_db_uri = 'postgresql:' + raw_db_uri[len(prefix):]
        SQLALCHEMY_DATABASE_URI = raw_db_uri
    else:
        if os.environ.get('VERCEL'):
            SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/jahangeer_chicken.db'
        else:
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'jahangeer_chicken.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Writable temporary directory for Vercel/serverless; instance/uploads for local development
    if os.environ.get('VERCEL'):
        UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'uploads')
    else:
        UPLOAD_FOLDER = os.path.join(basedir, 'instance', 'uploads')

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'svg'}
