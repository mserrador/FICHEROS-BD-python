"""
En este fichero vamos a ejecutar la opcion consultas,la opcion de consultas, pide al usuario por telcado el codigo
del cliente al que desaea consultar, con ese codigo el programa se encarga de buscar al cliente
al cual pertenece el codigo que nos proporciono el usuario, cuando se encuentra el registro 
del cliente, muestra todos sus datos
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
    codigoConsulta = int(input('Introduzca el codigo del cliente al cual desea consultar: '))


    if codigoConsulta > 1:
        # situamos el puntero
        fibi.seek(129*(codigoConsulta-1))
        registro = s.unpack(fibi.read(129))
    if codigoConsulta == 1:
        registro = s.unpack(fibi.read(129))
    
    situacion = registro[7].decode("UTF-8")
    if situacion != "b":
        codigo = registro[0]
        nombre = registro[1].decode("UTF-8")
        apellidos = registro[2].decode("UTF-8")
        dni = registro[3].decode("UTF-8")
        edad = registro[4]
        debe = registro[5]
        pagado = registro[6]    
        timestampSituacion = registro[8].decode("UTF-8")
        timestampBD = registro[9].decode("UTF-8")

        print('Cliente nº',codigo,'\n---------------------------')
        print("Nombre:",nombre)
        print("Apellidos:",apellidos)
        print("DNI:",dni)
        print("Edad:",edad)
        print("Debe:",debe)
        print("Pagado:",pagado)
        print("Situacion:",situacion)
        print("Fecha ultima modificacion de la situacion:",timestampSituacion)
        print("Fecha de la actualizacion en la BD:",timestampBD)
        print("\n")
    else:
        print('El cliente no existe o esta de baja')    

    opcion = input('Deseas consultar otro cliente? S/N: ').strip().upper()
    if opcion == "N":
        continuar = True



fibi.close()