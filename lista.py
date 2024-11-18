"""
En este fichero vamos a tratar con la opcion listar(desde-hasta), se va a encargar de pedir 
al usuario dos posiciones, desde y hasta, si no pasa el usuario ninguna posicion, el programa
lista todos los clientes teniendo en cuenta su situacion(si es b no los muestra), si le pasan
desde, lista desde la posicion que indico el usuario hasta el final, si solo le pasan hasta,
listara desde el primer cliente hasta que el que indico el usuario, y si pasan tanto desde 
como hasta listara teniendo en cuenta estas dos variables

esta opcion NUNCA listara un registro/cliente que en su campo situacion haya una "b"
"""
# importamos las librerias necesarias
import struct
import os
from datetime import datetime

# abrimos el fichero binario en modo lectura
fibi = open("fibi", "br")

# declaramos la estrucutra de los registros
s = struct.Struct("I 15s 50s 9s I f f 1s 18s 18s")

# vemos cuantos registros tiene el fichero binario
fichero = os.stat("fibi")
bytes = fichero.st_size
registros =  int(bytes/129)

desde = int(input('Desde que cliente quieres listar?(Escribe 0 para no establecer desde): '))
hasta = int(input('Hasta que cliente quieres listar?(Escribe 0 para no establecer hasta): '))
print()

if desde == 0 and hasta == 0:
    for i in range(registros):
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



elif desde != 0 and hasta == 0:
    for i in range(registros):
        registro = s.unpack(fibi.read(129))
        situacion = registro[7].decode("UTF-8")
        codigo = registro[0]
        
        if codigo >= desde:
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

elif desde == 0 and hasta != 0:
    for i in range(registros):
        registro = s.unpack(fibi.read(129))
        situacion = registro[7].decode("UTF-8")
        codigo = registro[0]
        
        if codigo <= hasta:
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


elif desde != 0 and hasta != 0:
    for i in range(registros):
        registro = s.unpack(fibi.read(129))
        situacion = registro[7].decode("UTF-8")
        codigo = registro[0]
        
        if codigo >= desde and codigo <= hasta:
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






# cerramos el fichero
fibi.close()