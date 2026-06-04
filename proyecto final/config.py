import os
from dotenv import load_dotenv
import create_key

load_dotenv()

class Configuracion:
    # Clave secreta
    SECRET_KEY = os.environ.get('SECRET_KEY') or create_key.secret_key()
    
    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://avnadmin:AVNS_07ai4AG3vYKvMn1JyFK@mysql-119f85db-cbtis-31cf.b.aivencloud.com:17610/defaultdb?ssl-mode=REQUIRED'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {}
    
    # Sesión
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', False)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
