import os
import tempfile
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Require SECRET_KEY from environment or generate random bytes for session safety
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    
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
