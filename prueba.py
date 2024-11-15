import struct # sirve para tratar los paquetes de el fichero binario
import os

with open("fibi","br+") as fibi:
    fichero = os.stat("fibi")
    bytes = fichero.st_size
    cantidadRegistros=int(bytes/127)
    s = struct.Struct("I 15s 50s 9s I f f 1s 18s 18s")
    if bytes <= 0:
        print("El fichero esta vacio, no se puede leer nada")
    # al ver que no esta vacio, comprobamos las 3 posibles situaciones
    else:
        print("hay ",int(bytes/129)," registros")

    for i in range(cantidadRegistros):
        codigo,nombre,apellidos,dni,edad,debe,pagado,situacion,timestampSituacion,timestampBD = s.unpack(fibi.read(129))
        print(codigo,nombre.decode("UTF-8"),situacion.decode("utf-8"),timestampSituacion.decode("UTF-8"))
