"""

"""
# importamos las librerias necesarias
import struct
import os
import sqlite3
from datetime import datetime




def actualizacionBD():
    """
    Este programa se encarga de actulizar los registros de la BD con los del fichero fibi que
    coincidan el el campo dni, tiene en cuenta la situcacion de los registros en fibi,
    guardara el timestamp del momento de la actualizacion tanto en la bd como en fibi,
    este programa ira leyendo registro a registro de fibi(los cuales su situacion es != "b")
    y comparando los dni con los de los registro de la BD, cuando encuentre dos dni iguales,
    actulizara los datos de los registros en la BD
    """

    # abrimos el fichero binario
    fibi = open("fibi","br+")

    # declaramos la estructura de un registro de fibi para poder trabajar con los registros
    s = struct.Struct("I 15s 50s 9s I f f 1s 18s 18s")

    # hacemos la conexion con la bd y su cursor
    DB_FILE = "gestion_clientes.db"
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # sacamos cuantos registros tiene fibi
    fichero = os.stat("fibi")
    bytes = fichero.st_size
    registros =  int(bytes/129)

    # hacemos un bucle que lea todos los registros de fibi

    for i in range(registros):
        #leemos un solo registro
        registro = s.unpack(fibi.read(129))

        # lo primero que comprobamos es la situacion del registro
        #  para ello debemos desempaquetarlo para pasarlo de binario a string

        situacionRegistro = registro[7]
        situacionRegistro = situacionRegistro.decode("UTF-8")

        # si situacionRegistro es igual a "a" o "m" seguimos con el programa, si no lo ignoramos
        if situacionRegistro ==  "a" or situacionRegistro == "m":
            # sacamos el dni del registro de fibi para posteriormente compararlo
            dniRegistro = registro[3]
            dniRegistro = dniRegistro.decode("UTF-8")

            # ahora debemos compararlo con el dni de un registro de la BD
            # Buscar cliente en la base de datos
            cursor.execute("SELECT * FROM clientes WHERE DNI = ?", (dniRegistro,))
            # solo debe existir un cliente con el mismo DNI
            cliente = cursor.fetchone()

            # en caso de que hay un match
            if cliente:
                print('cliente encontrado en la BD')

                # Actualizar datos en la BD
                nombre = registro[1].decode("UTF-8").strip("\x00")
                apellidos = registro[2].decode("UTF-8").strip("\x00")
                edad = registro[4]
                debe = registro[5]
                pagado = registro[6]
                fechaActual = datetime.now()
                timestamp = fechaActual.strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute('''
                    UPDATE clientes
                    SET Nombre = ?, Apellidos = ?, Edad = ?, Debe = ?, Pagado = ?, TimestampActualizacion = ?
                    WHERE DNI = ?
                ''', (nombre, apellidos, edad, debe, pagado, timestamp, dniRegistro))
                print(f"Cliente con DNI {dniRegistro} actualizado en la BD.")

                # Actualizar el timestamp en el registro de fibi
                timestampActualizacionBD = timestamp.encode("UTF-8")
                registro_actualizado = s.pack(registro[0],registro[1],registro[2],registro[3],registro[4],registro[5],registro[6],registro[7],registro[8],timestampActualizacionBD)

                # Posicionar el puntero en el registro a modificar y escribirlo
                fibi.seek(i * 129)
                fibi.write(registro_actualizado)
                print(f"Cliente con DNI {dniRegistro} actualizado en el fichero fibi.")


            else:
                print('cliente no encontrado en la BD')


    # cierro el fichero fibi
    fibi.close()

    # cierro la conexion con la BD
    conn.commit()
    conn.close()

def actualizacionConFite():
    """
    Este fichero se va a encargar de actulizar los registros del fibi que coincidan su campo codigo con los registro de fite que coincidan en el campo codigo,
    para ello el programa lo primero que hace es leer un registro del fite y comparar su campo codigo con los del fibi, si coinciden sustituye el registro 
    que hay en fibi por el de fite, ademas en fite hay que modificar el registro acutalizando el campo timestamp cuando se hace una actualizacion del fibi para que quede regisrado en fite

    """

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


def altas():
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

def altasBD():
    # Nombre del archivo de la base de datos
    DB_FILE = "gestion_clientes.db"

    # Conectar 
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()


    continuar = True

    clientes = []

    while continuar == True:


        dni = input('Introduce el dni: ')
        nombre = input('Introduce el nombre: ')
        apellidos = input('Introduce los apellidos: ')
        edad = int(input('Introduce la edad: '))
        debe= float(input('Introduce cuanto debe el cliente: '))
        pagado=float(input('Introduce cuanto ha pagado el cliente: '))
        timestamp = datetime.now()
        
        cliente = [dni,nombre,apellidos,edad,debe,pagado,timestamp]

        clientes.append(cliente)    


        #  preguntamos al usuario si desea hacer mas altas
        opcion = input("Desea hacer otra Alta S/N: ")   
        if opcion == "N":
            print(clientes.count)
            continuar = False 

        cursor.execute('''
            INSERT INTO clientes (DNI, Nombre, Apellidos, Edad, Debe, Pagado, TimestampActualizacion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', cliente)

    # Cerrar la conexión
    conn.commit()
    conn.close()