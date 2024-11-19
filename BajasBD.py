import sqlite3
"""
Elimina un cliente de la base de datos por DNI.
"""

# Nombre del archivo de la base de datos
DB_FILE = "gestion_clientes.db"

# Conectar 
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

dni = input("Introduce el DNI del cliente que deseas eliminar: ")

# Verificar si el cliente existe
cursor.execute("SELECT * FROM clientes WHERE DNI = ?", (dni,))
cliente = cursor.fetchone()

if cliente:
    # Confirmar eliminación
    print("\nCliente encontrado:")
    print(f"DNI: {cliente[0]}, Nombre: {cliente[1]}, Apellidos: {cliente[2]}")
    confirmacion = input("¿Estás seguro de que deseas eliminar este cliente? (S/N): ").strip().upper()

    if confirmacion == "S":
        cursor.execute("DELETE FROM clientes WHERE DNI = ?", (dni,))
        conn.commit()
        print("Cliente eliminado exitosamente.")
    else:
        print("Eliminación cancelada.")
else:
    print("No se encontró un cliente con ese DNI.")


# Cerrar la conexión
conn.close()