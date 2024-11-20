import sqlite3
from datetime import datetime

# Nombre del archivo de la base de datos
DB_FILE = "gestion_clientes.db"

# Conectar 
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

"""
Permite consultar un cliente específico por su DNI.
"""

# Solicitar el DNI del cliente a buscar
dni = input("Introduce el DNI del cliente que deseas consultar: ")
    
# Buscar cliente en la base de datos
cursor.execute("SELECT * FROM clientes WHERE DNI = ?", (dni,))
cliente = cursor.fetchone()
    
if cliente:
    print("\nCliente encontrado:")
    print(f"DNI: {cliente[0]}")
    print(f"Nombre: {cliente[1]}")
    print(f"Apellidos: {cliente[2]}")
    print(f"Edad: {cliente[3]}")
    print(f"Debe: {cliente[4]}")
    print(f"Pagado: {cliente[5]}")
    print(f"Última actualización: {cliente[6]}")
else:
    print("No se encontró ningún cliente con ese DNI.")

# Cerrar la conexión
conn.close()