import json
import os
from datetime import datetime

DATA_FILE = "data.json"

# Datos por defecto si el archivo no existe
DEFAULT_DATA = {
    "total_gastos": 0,
    "total_ingresos": 0,
    "total_ahorros": 0,
    "movimientos": [],
    "metas": []  # Nueva clave para almacenar metas
}

def load_data():
    """Carga los datos desde el archivo JSON"""
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        # En caso de error, crea un nuevo archivo
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA

def save_data(data):
    """Guarda los datos en el archivo JSON"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Funciones auxiliares para movimientos
def add_movimiento(tipo, monto, categoria, fecha):
    """Agrega un nuevo movimiento a los datos"""
    data = load_data()
    if tipo == "gasto":
        data["total_gastos"] += monto
    else:
        data["total_ingresos"] += monto
    
    # Formatear fecha si es necesario
    if isinstance(fecha, datetime):
        fecha = fecha.strftime("%Y-%m-%d %H:%M")
    
    data["movimientos"].append({
        "fecha": fecha,
        "tipo": tipo,
        "categoria": categoria,
        "monto": monto
    })
    save_data(data)

def get_totales():
    """Obtiene los totales de gastos, ingresos y ahorros"""
    data = load_data()
    return data["total_gastos"], data["total_ingresos"], data["total_ahorros"]

def get_movimientos():
    """Obtiene todos los movimientos"""
    return load_data()["movimientos"]

# Funciones auxiliares para metas
def get_metas():
    """Obtiene todas las metas almacenadas"""
    return load_data().get("metas", [])

def save_metas(metas):
    """Guarda la lista de metas en el archivo JSON"""
    data = load_data()
    data["metas"] = metas
    save_data(data)

def add_meta(nombre, cantidad, fecha_limite):
    """Agrega una nueva meta"""
    data = load_data()
    data["metas"].append({
        "nombre": nombre,
        "cantidad": cantidad,
        "progreso": 0.0,
        "fecha_limite": fecha_limite.strftime("%Y-%m-%d") if isinstance(fecha_limite, datetime) else fecha_limite
    })
    save_data(data)

def update_meta_progreso(meta_index, cantidad):
    """Actualiza el progreso de una meta"""
    data = load_data()
    if meta_index < len(data["metas"]):
        data["metas"][meta_index]["progreso"] += cantidad
        save_data(data)

def delete_meta(meta_index):
    """Elimina una meta"""
    data = load_data()
    if meta_index < len(data["metas"]):
        data["metas"].pop(meta_index)
        save_data(data)