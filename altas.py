# 1ER PASO importar las clases struct, os y datetime para poder trabajar
import struct # esta libreria nos permite hacer structuras para empaquetar y desempaquetar y asi escribir y leer registros en el fichero binario
import os # esta libreria nos permite ejecutar comandos del propio SO
from datetime import datetime # esta libreria genera un objeto con fechas, lo usamos apra los timestamps

# 2DO PASO abrimos el fichero binario
fibi = open("fibi","ba")
continuar = False

# 3ER PASO crear la structura del regiistro
s = struct.Struct("I 15s 50s 9s I f f 1s 18s 18s")

# vamos a sacar la longitud del fichero para poder hacer el campo codigo autoIncremental
fichero = os.stat("fibi")
bytes = fichero.st_size
codigo =  int(bytes/129)

while continuar == False:
    # codigo viene de leer la longitud del fichero binario, le sumamos 1 para que este campo sea auto incrmental
    codigo += 1

    # 4TO PASO crear las variables y rellenarlas 

    # ahora rellenamos las siguientes variables 
    nombre = input('Introduce el nombre del cliente: ')
    apellidos = input('Introduce los apellidos del cliente: ')
    dni= input('Introduce el DNI del cliente: ')
    edad= int(input('Introduce la edad del cliente: '))
    debe= float(input('Introduce cuanto debe el cliente: '))
    pagado=float(input('Introduce cuanto ha pagado el cliente: '))
    situacion = "a"
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
    registro = s.pack(codigo,nombre,apellidos,dni,edad,debe,pagado,situacion,timestampSituacion,timestampActualizacionBD)

    # finalmete escribimos el registro
    fibi.write(registro)  

    # preguntamos al usuario si desea hacer mas altas
    opcion = input("Desea hacer otra Alta S/N: ").strip().upper()   
    if opcion == "N":
        continuar = True  

# cerramos el fichero binario   
fibi.close()




