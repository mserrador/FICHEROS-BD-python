"""
En este fichero vamos a ejecutar la opcion BAJAS,la opcion de BAJAS, pide al usuario por telcado el DNI
del cliente al que desaea dar de baja, con ese DNI el programa se encarga de buscar al cliente
al cual pertenece el DNI que nos proporciono el usuario, cuando se encuentra el registro 
del cliente, se sustituye el contenido del campo "situacion" cambiando lo que hubiera en
ese campo por una "b", ademas se actualiza el timestamp de situacion con la fecha y hora 
del momento en que se cambia la situacion del cliente a baja.
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

# variable de control del bucle
continuar = False
while continuar == False:
    # despues de cada ejecucion del bucle situamos el puntero de lectura al principio
    fibi.seek(0)
    # pedimos al usuario que meta el DNI del cliente que quiere dar de baja
    dniBaja = input('Introduzca el DNI del cliente al cual desea dar de baja 00000000X: ')
    # esta varibale nos va a permitir verificar si se ha encontrado o no el cliente deseado y tambien nos permite informar al usuario
    encontrado = False
    # hacemos un bucle que recorra el fichero registro a registro y comprobamos el DNI de cada uno de los registros para dar de baja al indicado
    for i in range(registros):
        # hago que el puntero lea un registro entero
        registro = s.unpack(fibi.read(129))
        # saco el campo dni
        dni = registro[3]
        # hago decode al dni para poder comprarlo con el que introdujo el usuario
        dni = dni.decode("UTF-8")
        # comparo los dni
        if dni == dniBaja:
            # si coinciden creo un nuevo registro y lo sustituyo por el que ya habia
            fechaActual = datetime.now()
            timestampSituacion= fechaActual.strftime("%Y-%m-%d %H:%M:%S")
            # empaqueto el registro nuevo, dando de baja en situacion y con el timestamp de situacion
            nuevoRegistro = s.pack(registro[0],registro[1],registro[2],registro[3],
            registro[4],registro[5],registro[6],"b".encode("UTF-8"),
            timestampSituacion.encode("UTF-8"),registro[9])


            fibi.seek(i*129)
            fibi.write(nuevoRegistro)
            print('Se ha dado de baja al cliente ', registro[2].decode('UTF-8').strip("\x00") + ", "+registro[1].decode('UTF-8').strip("\x00"))
            encontrado = True

    if encontrado == False:
        print('No se ha encontrado ningun cliente con el DNI que has proporcionado')
        
    opcion = input('Deseas dar de baja a otro cliente? S/N: ').strip().upper()
    if opcion == "N":
        continuar = True



fibi.close()







    






fibi.close()




