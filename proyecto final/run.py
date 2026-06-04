from app import create_app
import os

if __name__ == '__main__':
    app = create_app()
    
    # Obtener puerto y host de variables de entorno o usar valores por defecto
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    debug = os.environ.get('FLASK_DEBUG', True)
    
    print(f"\n" + "="*60)
    print(f"  SISTEMA WEB ESCOLAR")
    print(f"  Servidor ejecutándose en: http://{host}:{port}")
    print(f"  Modo debug: {debug}")
    print("="*60 + "\n")
    
    app.run(host=host, port=port, debug=debug)
