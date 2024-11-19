"""
En este fichero vamos a tratar las modificaciones de la opcion "Modificaiones", en el que 
pedire al usuario que introduzca el DNI del cliente al cual deasea aplciar una modificaciones,
el programa buscara al cliente, si no existe el progrmaa se lo comunicara al usuario,
si existe, el programa pedira al usuario todos los datos del cliente con las modificaiones,
despues cambiara el campo situacion a  "m" y actualizara el time stamp del campo situacion
"""
# importamos las librerias necesarias
import struct
import os
from datetime import datetime

# abrimos el fichero binario en modo escritura y lectura
fibi = open("fibi", "br+")

# declaramos la estrucutra de los registros
s = struct.Struct("I 15s 50s 9s I f f 1s 18s 18s")

# vemos cuantos registros tiene el fichero binario
fichero = os.stat("fibi")
bytes = fichero.st_size
registros =  int(bytes/129)

continuar = True

while continuar == True:
    dniModificar = input('Introduce el DNI del cliente al cual quieres modificar 00000000X: ')
    fibi.seek(0)
    encontrado = False
    for i in range(registros):
        # hago que el puntero lea un registro entero
        registro = s.unpack(fibi.read(129))

        # saco el campo dni
        dni = registro[3]

        # hago decode al dni para poder compararlo con el que introdujo el usuario
        dni = dni.decode("UTF-8")

        # comparo los dni
        if dni == dniModificar:
            # si coinciden creo un nuevo registro y lo sustituyo por el que ya habia
            codigo = registro[0]
            nombre = input('Introduce el nombre del cliente: ')
            apellidos = input('Introduce los apellidos del cliente: ')
            dni= input('Introduce el DNI del cliente: ')
            edad= int(input('Introduce la edad del cliente: '))
            debe= float(input('Introduce cuanto debe el cliente: '))
            pagado=float(input('Introduce cuanto ha pagado el cliente: '))
            situacion = "m"
            fechaActual = datetime.now()
            timestampSituacion= fechaActual.strftime("%Y-%m-%d %H:%M:%S")
            timestampActualizacionBD=""

            # hacemos .encode a las variables que contengan un string para psarlas a binario
            nombre = nombre.encode("UTF-8")
            apellidos = apellidos.encode("UTF-8")
            dni = dni.encode("UTF-8")
            situacion = situacion.encode("UTF-8")
            timestampSituacion = timestampSituacion.encode("UTF-8")
            timestampActualizacionBD = timestampActualizacionBD.encode("UTF-8")

            # hacemos  y empaquetamos el registro
            registroModificado = s.pack(codigo,nombre,apellidos,dni,edad,debe,pagado,situacion,timestampSituacion,timestampActualizacionBD)

            fibi.seek(i*129)
            fibi.write(registroModificado)
            print('Se ha modificado el cliente ')

            encontrado = True

    if encontrado == False:
        print('Cliente no encontrado')

    opcion = input('Desea Modificar otro cliente? S/N: ').strip().upper()
    if opcion == "N":
        continuar = False

fibi.close()