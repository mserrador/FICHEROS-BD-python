# importar la calse struct
import struct

# hacemos la estructura con un total de 127 bytes
s = struct.Struct("I 15s 50s 9s I f f 1s 18s 18s")

# vamos a rellenar el molde usando variables 
# declaramos las variables

codigo=1# en verdad es autoincrmeental
nombre="mario"
apellidos="serrador garcia"
dni="17470026P"
edad=21
debe=6.9
pagado=9.6
situacion="a"
timestamp1="2024-11-13 18:00:00"
timestamp2="2033-11-13 18:00:00"

# ahora rellenado debemos enpaquetar las variables, las tipo numerico nos deja al ser numeros pero los caracteres hay que pasarlos a binario
# pasamos a binarios las s

nombreb=nombre.encode("UTF-8")
apellidosb=apellidos.encode("UTF-8")
dnib=dni.encode("UTF-8")
situacionb=situacion.encode("UTF-8")
timestamp1b=timestamp1.encode("UTF-8")
timestamp2b=timestamp2.encode("UTF-8")

# ahora empaquetamos las variables usando la estructura s previamente creada como molde
registro = s.pack(codigo,nombreb,apellidosb,dnib,edad,debe,pagado,situacionb,timestamp1b,timestamp2b)

print(registro)

# Ahora que esta empaquetado ya podemos crear el fichero binario, e introducirle estos datos con el write()
# abrimos el fichero binario
f = open("fibi","bw") # a la hora de abrir el fichero debemos indicar que es binario, si no nos saldra un error, ya que intentamos meter bytes a un fichero de texto
f.write(registro) # esto escribe el registro anterior que creamos

# cerramos 
f.close()

# asi hemos excrito en un fichero binario, ahora queremos leer un registro

# ahora gracias a la estructura que declaramos antes, podremos leer el fichero en python
# abrimos el fichero, si pongo una w me lo cargo el contenido del fichero, 
# si no calificamos(epsecificar) el tipo de fichero lo abre como tipo texto
f = open("fibi","br+") # lo hemos avierto de manera que le indicamos que es tipo binario, para leer y poder escribir con el +

regispL = f.read(127) # regispL tiene la L para poner un nombre difernete a la variable, le pasamos la longitud del registro, sabemos la longitud del registor ya que al hacer la estructura declaramos que fueran 18 bytes
print(regispL) # nos devuelv el registro, este registro esta empaquetado por lo que debemos desempaquetarlo para poder leerlo

registroU = s.unpack(regispL)
print(registroU) # aqui vemos que lo ha desempaquetado




