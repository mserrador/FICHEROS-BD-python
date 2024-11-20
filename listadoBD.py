import sqlite3
from datetime import datetime

# Nombre del archivo de la base de datos
DB_FILE = "gestion_clientes.db"

# Conectar 
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


"""
Lista clientes según un rango de índices utilizando SQL para filtrar.
"""
cursor = conn.cursor()
    
# Obtener la cantidad de registros para mostrar al usuario
cursor.execute("SELECT COUNT(*) FROM clientes")
total_registros = cursor.fetchone()[0]
    
if total_registros == 0:
    print("No hay clientes registrados.")
else:
    
    # Solicitar los índices
    desde = int(input(f"Introduce el índice de inicio (1 a {total_registros}): "))
    hasta = int(input(f"Introduce el índice de fin (1 a {total_registros}): "))
    
if desde < 1 or hasta > total_registros or desde > hasta:
    print("Rangos de índices no válidos.")
else:
    
    # Filtrar clientes con SQL
    cursor.execute('''
        SELECT * FROM clientes
        LIMIT ? OFFSET ?
    ''', (hasta - desde + 1, desde - 1))
    clientes = cursor.fetchall()
    
    print("\nClientes encontrados:")
    for cliente in clientes:
        print(f"DNI: {cliente[0]}, Nombre: {cliente[1]}, Apellidos: {cliente[2]}, Edad: {cliente[3]}, "
              f"Debe: {cliente[4]}, Pagado: {cliente[5]}, Última actualización: {cliente[6]}")
        
# Cerrar la conexión
conn.close()