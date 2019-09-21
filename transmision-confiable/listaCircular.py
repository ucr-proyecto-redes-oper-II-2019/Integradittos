import numpy as np 
#Fabian e Isaac
class listaCirular():

	list listaCircular = [0,0,0,0,0,0,0,0,0,0]
	int inicio = 0 
	int final = 0
	int numeroDePaqueteActual = 0

	#Se establece la posicion de inicio de la lista que este correspode al RN. 
	def establecerInicio(numeroDePaqueteInicio):
		numeroDePaqueteActual = numeroDePaqueteInicio		
		inicio = numeroPaqueteInicio % 10
	
	#Inserta un elemento en la lista, datos(los 516 bytes del paquete) y numeroDePaqueteAInsertar(El numero del paquete que se va a insertar).
	def insertar(datos ,int numeroDePaqueteAInsertar):#introducimos el nuevoPaquete
		if numeroDePaqueteAInsertar >= 10:#Si el paquete a insertar es mayor a 10 tenemos que aplicar el algoritmo para que la lista sea circular.
			posicionParaInsertar = ((numeroDePaqueteAInsertar - numeroDePaqueteActual) + inicio)- 10
		else:#Sino dejamos el numero de paqueta original
			posicioParaInsertar = numeroDePaqueteAInsertar
		listaCircular[posicionParaInsertar] = datos#Insertamos los bytes
		if posicioParaInsertar > final:
			final =  posicioParaInsertar 

	#retorna el los datos del numero de paquete, numeroDePaquete si no se encuentra retorna -1
	def getElemento(int numeroDePaquete)
		if numeroDePaquete >= 10:
			posicionABuscar = ((numeroDePaquete - numeroDePaqueteActual) + inicio) - 10#Calculamos la posicion en la que deberia estar ese paquete en el array circular
		else:
			posicionABuscar = numeroDePaquete
		dataBytes = listaCircular[posicionABuscar]
		dataBytes = dataBytes[1:3]#Sacamos los bytes donde se encuentra el numero de paquete.
		int.from_bytes(dataBytes, byorder='big')
		if dataBytes == numeroDePaquete:#comparamos que el numero de paquete deseado sea el que se encuentre en la posicion. 
			return listaCircular[posicionABuscar]
		else: 
			return -1

