"""
Este fichero se va a encargar de actulizar los registros del fibi que coincidan su campo codigo con los registro de fite que coincidan en el campo codigo,
para ello el programa lo primero que hace es leer un registro del fite y comparar su campo codigo con los del fibi, si coinciden sustituye el registro 
que hay en fibi por el de fite, ademas en fite hay que modificar el registro acutalizando el campo timestamp cuando se hace una actualizacion del fibi para que quede regisrado en fite

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
registrosB =  int(bytesB/129)


# vemos cuantos registros tiene el fichero de texto
ficheroT = os.stat("fite")
bytesT = ficheroT.st_size
registrosT =  int(bytesT/34)

contador = 0

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
    
    fibi.seek(0)
    for j in range(registrosB):
        # hago que el puntero lea un registro entero
        registroB = s.unpack(fibi.read(129))

        # saco el campo codigo del fichero binario
        codigoB = registroB[0]

        if codigoT == codigoB:
            # aqui hemos encontrado 2 registros que coinciden en el campo codigo
            # hay que sustituir el campo del dni en fibi
            
            # guardamos en una variable el dni de el registro de fite
            dniT = registroT[5]+registroT[6]+registroT[7]+registroT[8]+registroT[9]+registroT[10]+registroT[11]+registroT[12]+registroT[13]

            # creamos el nuevo registro a guardar en fibi, pero lleva el dni del fite
            fechaActual = datetime.now()
            timestampSituacion= fechaActual.strftime("%Y-%m-%d %H:%M:%S")
            registroNuevo=s.pack(registroB[0],registroB[1],registroB[2],dniT.encode("UTF-8"),registroB[4],registroB[5],registroB[6],"m".encode("UTF-8"),timestampSituacion.encode("UTF-8"),registroB[9])

            # tambien creamos el registro que se va a guardar en fite sustituyendo el campo timestamp
            cadena = "{0:05}{1:9s}{2:19s}{c}".format(codigoT,dniT,timestampSituacion,c="\n")
            fite.seek(i*34)
            fite.write(cadena)

            # ajustamos el puntero para que sobreescriba el registro previeo
            fibi.seek(j*129)
            # sobreescribimos el registro
            fibi.write(registroNuevo)
            contador +=1


print("se han modificado",contador,"clientes")           

# cerramos los ficheros
fibi.close()
fite.close()