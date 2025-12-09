import firebase_admin
from firebase_admin import credentials, auth
import os
DATABASE_URL = 'https://greenway-450aa-default-rtdb.firebaseio.com'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CRED_PATH = os.path.join(BASE_DIR, '..', 'serviceAccountKey.json')

try:
    cred = credentials.Certificate(CRED_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': DATABASE_URL
    })
    admin_auth = auth
    print("SDK de Admin de Firebase inicializado con éxito.")
    
except FileNotFoundError:
    print("="*50)
    print(f"ERROR: No se encontró el archivo '{CRED_PATH}'.")
    print("Por favor, descarga tu 'serviceAccountKey.json' desde la Consola de Firebase")
    print("y colócalo en tu carpeta 'data/'.")
    print("="*50)
    admin_auth = None
    
except Exception as e:
    print(f"Error inicializando el SDK de Admin: {e}")
    admin_auth = None