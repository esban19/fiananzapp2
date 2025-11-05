# utils/auth.py
import json
import os
import hashlib
from pathlib import Path
import uuid
import datetime

# Obtener la ruta del directorio actual
BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = BASE_DIR / "users.json"

def load_users():
    """Carga los usuarios desde el archivo JSON"""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)
        return []
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error leyendo users.json, creando nuevo archivo")
        with open(USERS_FILE, "w") as f:
            json.dump([], f)
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []

def save_users(users):
    """Guarda la lista de usuarios en el archivo JSON"""
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
        return True
    except Exception as e:
        print(f"Error guardando usuarios: {e}")
        return False

def hash_password(password):
    """Devuelve el hash SHA-256 de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(email, password):
    """Autentica un usuario usando el archivo JSON"""
    users = load_users()
    email = email.strip().lower()
    hashed_password = hash_password(password)
    
    for user in users:
        if user["email"].lower() == email and user["password"] == hashed_password:
            return True
    return False

def get_user(email):
    """Obtiene un usuario por su email"""
    users = load_users()
    email = email.strip().lower()
    for user in users:
        if user["email"].lower() == email:
            return user
    return None

def get_user_by_id(user_id):
    """Obtiene un usuario por su ID"""
    users = load_users()
    for user in users:
        if user["id"] == user_id:
            return user
    return None

def register_user(name, email, password):
    """Registra un nuevo usuario"""
    users = load_users()
    email = email.strip().lower()
    
    # Verificar si el usuario ya existe
    for user in users:
        if user["email"].lower() == email:
            return False
    
    # Crear nuevo usuario con ID único
    new_user = {
        "id": str(uuid.uuid4()),  # ID único universal
        "name": name,
        "email": email,
        "password": hash_password(password),
        "created_at": datetime.datetime.now().isoformat(),
        "last_login": None,
        "profile_pic": None,
        "currency": "USD",
        "notification_enabled": True
    }
    
    users.append(new_user)
    if save_users(users):
        return True
    return False

def update_user(user_id, updates):
    """Actualiza información de un usuario"""
    users = load_users()
    updated = False
    
    for user in users:
        if user["id"] == user_id:
            for key, value in updates.items():
                # No permitir actualización de ID o contraseña directamente
                if key not in ["id", "password"]:
                    user[key] = value
            updated = True
            break
    
    if updated:
        return save_users(users)
    return False

def update_user_name(user_id, new_name):
    """Actualiza el nombre de un usuario"""
    return update_user(user_id, {"name": new_name})

def update_user_password(user_id, current_password, new_password):
    """Actualiza la contraseña de un usuario"""
    users = load_users()
    current_hashed = hash_password(current_password)
    new_hashed = hash_password(new_password)
    
    for user in users:
        if user["id"] == user_id and user["password"] == current_hashed:
            user["password"] = new_hashed
            if save_users(users):
                return True
    return False

def update_user_profile_pic(user_id, image_path):
    """Actualiza la foto de perfil de un usuario"""
    return update_user(user_id, {"profile_pic": image_path})

def update_user_currency(user_id, currency):
    """Actualiza la moneda preferida del usuario"""
    return update_user(user_id, {"currency": currency})

def update_last_login(user_id):
    """Actualiza la última fecha de inicio de sesión"""
    return update_user(user_id, {"last_login": datetime.datetime.now().isoformat()})

def delete_user(user_id):
    """Elimina un usuario por su ID"""
    users = load_users()
    new_users = [user for user in users if user["id"] != user_id]
    
    if len(new_users) < len(users):
        return save_users(new_users)
    return False

def add_admin_user():
    """Agrega un usuario admin si no existe"""
    users = load_users()
    admin_email = "admin@finanzapp.com"
    
    # Verificar si el admin ya existe
    for user in users:
        if user["email"] == admin_email:
            return
    
    # Crear admin
    admin_user = {
        "id": "admin-001",
        "name": "Administrador",
        "email": admin_email,
        "password": hash_password("1234"),
        "created_at": datetime.datetime.now().isoformat(),
        "last_login": None,
        "profile_pic": None,
        "currency": "USD",
        "notification_enabled": True
    }
    
    users.append(admin_user)
    save_users(users)

# Crear usuario admin al importar el módulo
add_admin_user()