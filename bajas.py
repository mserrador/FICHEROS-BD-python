"""
En este fichero vamos a ejecutar la opcion BAJAS,la opcion de BAJAS, pide al usuario por telcado el codigo
del cliente al que desaea dar de baja, con ese codigo el programa se encarga de buscar al cliente
al cual pertenece el codigo que nos proporciono el usuario, cuando se encuentra el registro 
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
    # pedimos al usuario que meta el codigo del cliente que quiere dar de baja
    codigoBaja = int(input('Introduzca el codigo del cliente al cual desea dar de baja: '))


    if codigoBaja > 1:
            # situamos el puntero
            fibi.seek(129*(codigoBaja-1))
            registro = s.unpack(fibi.read(129))
    if codigoBaja == 1:
        registro = s.unpack(fibi.read(129))
       
    fechaActual = datetime.now()
    timestampSituacion= fechaActual.strftime("%Y-%m-%d %H:%M:%S")
    # empaqueto el registro nuevo, dando de baja en situacion y con el timestamp de situacion
    nuevoRegistro = s.pack(registro[0],registro[1],registro[2],registro[3],
    registro[4],registro[5],registro[6],"b".encode("UTF-8"),
    timestampSituacion.encode("UTF-8"),registro[9])

    fibi.seek(129*(codigoBaja-1))
    fibi.write(nuevoRegistro)
    print('Se ha dado de baja al cliente ', registro[2].decode('UTF-8') + ", "+registro[1].decode('UTF-8'))

    opcion = input('Deseas dar de baja a otro cliente? S/N: ').strip().upper()
    if opcion == "N":
        continuar = True



fibi.close()
