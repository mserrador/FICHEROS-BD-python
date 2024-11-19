import sqlite3
from datetime import datetime

# Nombre del archivo de la base de datos
DB_FILE = "gestion_clientes.db"

# Conectar 
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


continuar = True

clientes = []

while continuar == True:


    dni = input('Introduce el dni: ')
    nombre = input('Introduce el nombre: ')
    apellidos = input('Introduce los apellidos: ')
    edad = int(input('Introduce la edad: '))
    debe= float(input('Introduce cuanto debe el cliente: '))
    pagado=float(input('Introduce cuanto ha pagado el cliente: '))
    timestamp = datetime.now()
    
    cliente = [dni,nombre,apellidos,edad,debe,pagado,timestamp]

    clientes.append(cliente)    


    #  preguntamos al usuario si desea hacer mas altas
    opcion = input("Desea hacer otra Alta S/N: ")   
    if opcion == "N":
        print(clientes.count)
        continuar = False 

    cursor.execute('''
        INSERT INTO clientes (DNI, Nombre, Apellidos, Edad, Debe, Pagado, TimestampActualizacion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', cliente)

# Cerrar la conexión
conn.commit()
conn.close()