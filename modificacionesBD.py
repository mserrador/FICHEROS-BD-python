import sqlite3
from datetime import datetime

# Nombre del archivo de la base de datos
DB_FILE = "gestion_clientes.db"

# Conectar 
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

"""
Modifica un cliente existente en la base de datos.
"""
cursor = conn.cursor()
    
# Solicitar DNI del cliente a modificar
dni = input("Introduce el DNI del cliente que deseas modificar: ")
    
# Verificar si el cliente existe
cursor.execute("SELECT * FROM clientes WHERE DNI = ?", (dni,))
cliente = cursor.fetchone()
    
if cliente:
    # Mostrar datos actuales del cliente
    print("\nCliente encontrado:")
    print(f"DNI: {cliente[0]}, Nombre: {cliente[1]}, Apellidos: {cliente[2]}, Edad: {cliente[3]}, Debe: {cliente[4]}, Pagado: {cliente[5]}")
        
    # Solicitar nuevos datos
    print("\nIntroduce los nuevos datos (presiona ENTER para mantener el valor actual):")
    nombre = input(f"Nombre [{cliente[1]}]: ") or cliente[1]
    apellidos = input(f"Apellidos [{cliente[2]}]: ") or cliente[2]
    edad = input(f"Edad [{cliente[3]}]: ") or cliente[3]
    debe = input(f"Debe [{cliente[4]}]: ") or cliente[4]
    pagado = input(f"Pagado [{cliente[5]}]: ") or cliente[5]
    
    # Asegurar tipos correctos
    edad = int(edad) if edad else cliente[3]
    debe = float(debe) if debe else cliente[4]
    pagado = float(pagado) if pagado else cliente[5]
    
    # Actualizar timestamp
    timestamp_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Actualizar registro en la base de datos
    cursor.execute('''
        UPDATE clientes 
        SET Nombre = ?, Apellidos = ?, Edad = ?, Debe = ?, Pagado = ?, TimestampActualizacion = ?
        WHERE DNI = ?
    ''', (nombre, apellidos, edad, debe, pagado, timestamp_actualizacion, dni))
    conn.commit()
    print("El cliente ha sido modificado exitosamente.")
else:
    print("No se encontró un cliente con ese DNI.")

# Cerrar la conexión
conn.close()