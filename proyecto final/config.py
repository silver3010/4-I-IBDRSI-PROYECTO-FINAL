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
        'mysql+pymysql://avnadmin:AVNS_WE9_KEHQsbc15PD5FHE@mysql-f382ebf-cbtis.b.aivencloud.com:26910/defaultdb'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {}
    
    # Sesión
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', False)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
