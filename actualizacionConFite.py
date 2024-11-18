"""
Este fichero se va a encargar de actulizar los registros del fibi que coincidan su campo codigo con los registro de fite que coincidan en el campo codigo,
para ello el programa lo primero que hace es leer un registro del fite y comparar su campo codigo con los del fibi, si coinciden sustituye el registro 
que hay en fibi por el de fite
"""
# importamos las librerias necesarias
import struct
import os
from datetime import datetime

# abrimos el fichero binario en modo escritura y lectura
fibi = open("fibi", "br+")

# abrimos el fichero texto en modo escritura y lectura
fite = open("fite", "r+")

# declaramos la estrucutra de los registros
s = struct.Struct("I 15s 50s 9s I f f 1s 18s 18s")

# vemos cuantos registros tiene el fichero binario
ficheroB = os.stat("fibi")
bytesB = ficheroB.st_size
registrosB =  int(bytes/129)


# vemos cuantos registros tiene el fichero de texto
ficheroT = os.stat("fite")
bytesT = ficheroT.st_size
registrosT =  int(bytes/34)

for i in range(registrosT):
    # leo un registro
    registroT = fite.readline()

    # saco el campo codigo del fichero de texto
    codigoT = registroT[0]+registroT[1]+registroT[2]+registroT[3]+registroT[4]

    # quito los 0 sobrantes del campo codigo para poder compararlo
    codigoT = codigoT.strip("0")

    # parseo el codigoT a int para poder compararlo con el de fibi
    codigoT = int(codigoT)

    # creamos la variable que va a guardar el codigo de fibi
    codigoB = 0

    nomas = 0

    if nomas < bytesB:
        while codigoT != codigoB:
            # hago que el puntero lea un registro entero
            registro = s.unpack(fibi.read(129))
            nomas = nomas+129

            # saco el campo codigo del fichero binario
            codigoB = registro[0]

            if codigoT == codigoB:
                print('coincidencia encontrada')






























# cerramos los ficheros
fibi.close()
fite.close()