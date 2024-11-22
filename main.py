"""

"""
# importamos las librerias necesarias
import struct
import os
import sqlite3
from datetime import datetime
import pickle

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

def bajas():
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

def bajasBD():
    # Nombre del archivo de la base de datos
    DB_FILE = "gestion_clientes.db"

    # Conectar 
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    dni = input("Introduce el DNI del cliente que deseas eliminar: ")

    # Verificar si el cliente existe
    cursor.execute("SELECT * FROM clientes WHERE DNI = ?", (dni,))
    cliente = cursor.fetchone()

    if cliente:
        # Confirmar eliminación
        print("\nCliente encontrado:")
        print(f"DNI: {cliente[0]}, Nombre: {cliente[1]}, Apellidos: {cliente[2]}")
        confirmacion = input("¿Estás seguro de que deseas eliminar este cliente? (S/N): ").strip().upper()

        if confirmacion == "S":
            cursor.execute("DELETE FROM clientes WHERE DNI = ?", (dni,))
            conn.commit()
            print("Cliente eliminado exitosamente.")
        else:
            print("Eliminación cancelada.")
    else:
        print("No se encontró un cliente con ese DNI.")


    # Cerrar la conexión
    conn.close()

def consultas():
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

def consultasBD():
     # Nombre del archivo de la base de datos
    DB_FILE = "gestion_clientes.db"

    # Conectar 
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    """
    Permite consultar un cliente específico por su DNI.
    """

    # Solicitar el DNI del cliente a buscar
    dni = input("Introduce el DNI del cliente que deseas consultar: ")
        
    # Buscar cliente en la base de datos
    cursor.execute("SELECT * FROM clientes WHERE DNI = ?", (dni,))
    cliente = cursor.fetchone()
        
    if cliente:
        print("\nCliente encontrado:")
        print(f"DNI: {cliente[0]}")
        print(f"Nombre: {cliente[1]}")
        print(f"Apellidos: {cliente[2]}")
        print(f"Edad: {cliente[3]}")
        print(f"Debe: {cliente[4]}")
        print(f"Pagado: {cliente[5]}")
        print(f"Última actualización: {cliente[6]}")
    else:
        print("No se encontró ningún cliente con ese DNI.")

    # Cerrar la conexión
    conn.close()

def listar():
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

def listarBD():
    # Nombre del archivo de la base de datos
    DB_FILE = "gestion_clientes.db"

    # Conectar 
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()


    """
    Lista clientes según un rango de índices utilizando SQL para filtrar.
    """
    cursor = conn.cursor()
        
    # Obtener la cantidad de registros para mostrar al usuario
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_registros = cursor.fetchone()[0]
        
    if total_registros == 0:
        print("No hay clientes registrados.")
    else:
        
        # Solicitar los índices
        desde = int(input(f"Introduce el índice de inicio (1 a {total_registros}): "))
        hasta = int(input(f"Introduce el índice de fin (1 a {total_registros}): "))
        
    if desde < 1 or hasta > total_registros or desde > hasta:
        print("Rangos de índices no válidos.")
    else:
        
        # Filtrar clientes con SQL
        cursor.execute('''
            SELECT * FROM clientes
            LIMIT ? OFFSET ?
        ''', (hasta - desde + 1, desde - 1))
        clientes = cursor.fetchall()
        
        print("\nClientes encontrados:")
        for cliente in clientes:
            print(f"DNI: {cliente[0]}, Nombre: {cliente[1]}, Apellidos: {cliente[2]}, Edad: {cliente[3]}, "
                f"Debe: {cliente[4]}, Pagado: {cliente[5]}, Última actualización: {cliente[6]}")
            
    # Cerrar la conexión
    conn.close()

def modificaciones():
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

def modificacionesBD():
    # Nombre del archivo de la base de datos
    DB_FILE = "gestion_clientes.db"

    # Conectar 
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    """
    Modifica un cliente existente en la base de datos.
    """
    cursor = conn.cursor()
        
    # Solicitar DNI del cliente a modificar
    dni = input("Introduce el DNI del cliente que deseas modificar: ")
        
    # Verificar si el cliente existe
    cursor.execute("SELECT * FROM clientes WHERE DNI = ?", (dni,))
    cliente = cursor.fetchone()
        
    if cliente:
        # Mostrar datos actuales del cliente
        print("\nCliente encontrado:")
        print(f"DNI: {cliente[0]}, Nombre: {cliente[1]}, Apellidos: {cliente[2]}, Edad: {cliente[3]}, Debe: {cliente[4]}, Pagado: {cliente[5]}")
            
        # Solicitar nuevos datos
        print("\nIntroduce los nuevos datos (presiona ENTER para mantener el valor actual):")
        nombre = input(f"Nombre [{cliente[1]}]: ") or cliente[1]
        apellidos = input(f"Apellidos [{cliente[2]}]: ") or cliente[2]
        edad = input(f"Edad [{cliente[3]}]: ") or cliente[3]
        debe = input(f"Debe [{cliente[4]}]: ") or cliente[4]
        pagado = input(f"Pagado [{cliente[5]}]: ") or cliente[5]
        
        # Asegurar tipos correctos
        edad = int(edad) if edad else cliente[3]
        debe = float(debe) if debe else cliente[4]
        pagado = float(pagado) if pagado else cliente[5]
        
        # Actualizar timestamp
        timestamp_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Actualizar registro en la base de datos
        cursor.execute('''
            UPDATE clientes 
            SET Nombre = ?, Apellidos = ?, Edad = ?, Debe = ?, Pagado = ?, TimestampActualizacion = ?
            WHERE DNI = ?
        ''', (nombre, apellidos, edad, debe, pagado, timestamp_actualizacion, dni))
        conn.commit()
        print("El cliente ha sido modificado exitosamente.")
    else:
        print("No se encontró un cliente con ese DNI.")

    # Cerrar la conexión
    conn.close()


class Situacion:
    def __init__(self,debeTotal,haberTotal,codigo,timeStamp):
        self.debeTotal = debeTotal
        self.haberTotal = haberTotal
        self.codigo = codigo
        self.timeStamp = timeStamp
    def mostrarDatos(self):
        print()
        print("Debe Total:",self.debeTotal)
        print("haber Total:",self.haberTotal)
        print("Ultimo codigo del cliente:",self.codigo)
        print("TimeStamp de la ultima actualizacion:", self.timeStamp.decode("UTF-8"))
        print()




def informeSituacionActual():
    # abrimos el fichero binario
    fibi = open("fibi","br")
    continuar = False

    # crear la structura del regiistro
    s = struct.Struct("I 15s 50s 9s I f f 1s 18s 18s")

    # vamos a sacar la longitud del fichero
    fichero = os.stat("fibi")
    bytes = fichero.st_size
    registros =  int(bytes/129)

    # declaramos las variables para rellenar el objeto que se guardara en el pickle
    debeTotal = 0
    haberTotal = 0
    codigo = 0
    fechaActual = datetime.now()
    timeStamp = fechaActual.strftime("%Y-%m-%d %H:%M:%S")

    # hacemos un bucle para rellenar las variables
    for i in range(registros):
        registro = s.unpack(fibi.read(129))

        codigo = registro[0]
        debeTotal = debeTotal + registro[5]
        haberTotal = haberTotal + registro[6]


    # rellenamos el molde de la calse situacion
    situacion1 = Situacion(debeTotal,haberTotal,codigo,timeStamp.encode("UTF-8"))

    # abrimos el fichero del pickle
    fiPickle=open("fiPickle","bw")

    # escribimos el pickle en el fichero
    # el primer parametro es el objeto y el segundo el fichero
    pickle.dump(situacion1, fiPickle)

    fiPickle.close()

    opcion = input('Deseas ver el contenido del pickle? S/N: ')

    if opcion == "S":
        # abrimos el fichero del pickle
        fiPickle=open("fiPickle","br")

        situacion = pickle.load(fiPickle)

        situacion.mostrarDatos()

        fiPickle.close()



def menuBinario():
    continuar = True
    while continuar == True:
        print('---MENU FICHERO BINARIO---')
        print('Dar de alta: 1')
        print('Dar de baja: 2')
        print('Modificaciones: 3')
        print('consultas: 4')
        print('Lista(desde-hasta): 5')
        print('Actualizacion con fichero texto: 6')
        print('Actualizacion de la B.D: 7')
        print('Informe situacion actual: 8')
        print('Volver: 0')
        opcion = int(input('Selecciona una opcion: '))

        if opcion == 0:
            continuar = False
        elif opcion == 1:
            print()
            altas()
        elif opcion == 2:
            print()
            bajas()
        elif opcion == 3:
            print()
            modificaciones()
        elif opcion == 4:
            print()
            consultas()
        elif opcion == 5:
            print()
            listar()
        elif opcion == 6:
            print()
            actualizacionConFite()
        elif opcion == 7:
            print()
            actualizacionBD()
        elif opcion == 8:
            print()
            informeSituacionActual()

def menuBD():
    continuar = True
    while continuar == True:
        print('---MENU BD---')
        print('Dar de alta: 1')
        print('Dar de baja: 2')
        print('Modificaciones: 3')
        print('consultas: 4')
        print('Lista(desde-hasta): 5')
        print('Volver: 0')
        opcion = int(input('Selecciona una opcion: '))

        if opcion == 0:
            continuar = False
        elif opcion == 1:
            print()
            altasBD()
        elif opcion == 2:
            print()
            bajasBD()
        elif opcion == 3:
            print()
            modificacionesBD()
        elif opcion == 4:
            print()
            consultasBD()
        elif opcion == 5:
            print()
            listarBD()
 

continuar = True
while continuar == True:
    print('---MENU---')
    print('MENU BINARIO: 1')
    print('MENU BD: 2')
    print('Salir: 0')
    opcion = int(input('Selecciona una opcion: '))

    if opcion == 0:
        continuar = False
    elif opcion == 1:
        print()
        menuBinario()
    elif opcion == 2:
        print()
        menuBD()
