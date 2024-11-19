"""
En este fichero vamos a tratar las modificaciones de la opcion "Modificaiones", en el que 
pedire al usuario que introduzca el codigo del cliente al cual deasea aplciar una modificacion,
el programa buscara al cliente, si no existe el programa se lo comunicara al usuario,
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
    codigoModificar = int(input('Introduce el codigo del cliente al cual quieres modificar: '))
    
    if codigoModificar <= registros:
        fibi.seek(0)
    
        if codigoModificar > 1:
            # situamos el puntero
            fibi.seek(129*(codigoModificar-1))
        if codigoModificar == 1:
            fibi.seek(0)


        

        # hago el nuevo registro
        codigo = codigoModificar
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

        fibi.write(registroModificado)
        print('Se ha modificado el cliente ')

    else:
        print("El codigo que has introducido no pertenece a ningun registro")

    
    




    opcion = input('Desea Modificar otro cliente? S/N: ').strip().upper()
    if opcion == "N":
        continuar = False

fibi.close()