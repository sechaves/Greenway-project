import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
from data.firebase_config import db 
from data.firebase_admin import admin_auth
from domain.models import Admin
EMAIL_DEL_USUARIO_A_PROMOVER = "sechaves@unal.edu.co"
NUEVO_ROL = "admin"
def promover_a_admin():
    """
    Script de una sola vez para promover un usuario existente a Admin.
    """
    if not admin_auth:
        print("ERROR: El SDK de Admin (firebase_admin) no se inicializó.")
        print("Asegúrate de tener 'serviceAccountKey.json' en la carpeta 'data/'.")
        return

    try:
        print(f"Buscando usuario: {EMAIL_DEL_USUARIO_A_PROMOVER}...")
        user = admin_auth.get_user_by_email(EMAIL_DEL_USUARIO_A_PROMOVER)
        user_id = user.uid
        print(f"Usuario encontrado. ID: {user_id}")
        print(f"Asignando rol '{NUEVO_ROL}' como Custom Claim...")
        admin_auth.set_custom_user_claims(user_id, {'role': NUEVO_ROL})
        print(f"Creando instancia de Admin y guardando en nodo 'admins/'...")
        
        nombre_admin = user.display_name or EMAIL_DEL_USUARIO_A_PROMOVER.split('@')[0]
        
        admin_instance = Admin(
            user_id=user_id,
            nombre=nombre_admin,
            email=user.email
        )
        admin_instance.save_to_db(db)

        print("\n" + "="*30)
        print("¡ÉXITO!")
        print(f"El usuario {EMAIL_DEL_USUARIO_A_PROMOVER} ahora tiene el rol de '{NUEVO_ROL}'.")
        print("Sus datos han sido guardados en el nodo 'admins/'.")
        print("Por favor, cierra sesión y vuelve a iniciar sesión en la app para ver los cambios.")
        print("="*30 + "\n")

    except Exception as e:
        print("\n" + "!"*30)
        print(f"ERROR: No se pudo promover al usuario.")
        print(f"Detalle: {e}")
        print("Asegúrate de que el email esté escrito correctamente.")
        print("Y que ese usuario YA EXISTA en 'Firebase Authentication' (puedes crearlo con el formulario de registro de tu app primero).")
        print("!"*30 + "\n")

if __name__ == '__main__':
    if EMAIL_DEL_USUARIO_A_PROMOVER == "tu-email-de-admin@gmail.com":
        print("ERROR: Por favor, edita el archivo 'seed_admin.py' y pon tu email.")
    else:
        promover_a_admin()

