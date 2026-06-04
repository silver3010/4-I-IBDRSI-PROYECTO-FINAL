import os
import hashlib
import secrets

def secret_key():
    """
    Genera y reutiliza una clave secreta para Flask.
    Si no existe, la crea y la guarda en .secret_key
    """
    secret_file = '.secret_key'
    
    if os.path.exists(secret_file):
        with open(secret_file, 'r') as f:
            return f.read()
    else:
        # Generar una nueva clave segura
        key = secrets.token_hex(32)
        with open(secret_file, 'w') as f:
            f.write(key)
        return key
