"""
Este programa se encarga de actulizar los registros de la BD con los del fichero fibi que
coincidan el el campo dni, tiene en cuenta la situcacion de los registros en fibi,
guardara el timestamp del momento de la actualizacion tanto en la bd como en fibi,
este programa ira leyendo registro a registro de fibi(los cuales su situacion es != "b")
y comparando los dni con los de los registro de la BD, cuando encuentre dos dni iguales,
actulizara los datos de los registros en la BD
"""
# importamos las librerias necesarias
import struct
import os
import sqlite3
from datetime import datetime

# abrimos el fichero binario
fibi = open("fibi","br+")

# declaramos la estructura de un registro de fibi para poder trabajar con los registros
s = struct.Struct("I 15s 50s 9s I f f 1s 18s 18s")

# hacemos la conexion con la bd y su cursor
DB_FILE = "gestion_clientes.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# sacamos cuantos registros tiene fibi
fichero = os.stat("fibi")
bytes = fichero.st_size
registros =  int(bytes/129)

# hacemos un bucle que lea todos los registros de fibi

for i in range(registros):
    #leemos un solo registro
    registro = s.unpack(fibi.read(129))

    # lo primero que comprobamos es la situacion del registro
    #  para ello debemos desempaquetarlo para pasarlo de binario a string

    situacionRegistro = registro[7]
    situacionRegistro = situacionRegistro.decode("UTF-8")

    # si situacionRegistro es igual a "a" o "m" seguimos con el programa, si no lo ignoramos
    if situacionRegistro ==  "a" or situacionRegistro == "m":
        # sacamos el dni del registro de fibi para posteriormente compararlo
        dniRegistro = registro[3]
        dniRegistro = dniRegistro.decode("UTF-8")

        # ahora debemos compararlo con el dni de un registro de la BD
        # Buscar cliente en la base de datos
        cursor.execute("SELECT * FROM clientes WHERE DNI = ?", (dniRegistro,))
        # solo debe existir un cliente con el mismo DNI
        cliente = cursor.fetchone()

        # en caso de que hay un match
        if cliente:
            print('cliente encontrado en la BD')

            # Actualizar datos en la BD
            nombre = registro[1].decode("UTF-8").strip("\x00")
            apellidos = registro[2].decode("UTF-8").strip("\x00")
            edad = registro[4]
            debe = registro[5]
            pagado = registro[6]
            fechaActual = datetime.now()
            timestamp = fechaActual.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute('''
                UPDATE clientes
                SET Nombre = ?, Apellidos = ?, Edad = ?, Debe = ?, Pagado = ?, TimestampActualizacion = ?
                WHERE DNI = ?
            ''', (nombre, apellidos, edad, debe, pagado, timestamp, dniRegistro))
            print(f"Cliente con DNI {dniRegistro} actualizado en la BD.")

            # Actualizar el timestamp en el registro de fibi
            timestampActualizacionBD = timestamp.encode("UTF-8")
            registro_actualizado = s.pack(registro[0],registro[1],registro[2],registro[3],registro[4],registro[5],registro[6],registro[7],registro[8],timestampActualizacionBD)

            # Posicionar el puntero en el registro a modificar y escribirlo
            fibi.seek(i * 129)
            fibi.write(registro_actualizado)
            print(f"Cliente con DNI {dniRegistro} actualizado en el fichero fibi.")


        else:
            print('cliente no encontrado en la BD')


# cierro el fichero fibi
fibi.close()

# cierro la conexion con la BD
conn.commit()
conn.close()