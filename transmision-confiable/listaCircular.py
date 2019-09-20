import numpy as np 
#Fabian e Isaa
class listaCirular():

	list listaCircular 
	int inicio = 0 
	int final = 0
	int numeroDePaqueteActual = 0

	#Se establece la posicion de inicio de la lista que este correspode al RN. 
	def establecerInicio(numeroDePaqueteInicio):
		numeroDePaqueteActual = numeroDePaqueteInicio		
		inicio = numeroPaqueteInicio % 10

	#Inserta un elemento en la lista, datos(los 516 bytes del paquete) y numeroDePaqueteAInsertar(El numero del paquete que se va a insertar).
	def insertar(datos ,int numeroDePaqueteAInsertar):#introducimos el nuevoPaquete
		posicionParaInsertar = (numeroDePaqueteAInsertar - numeroDePaqueteActual) + inicio
		posicionParaInsertar = posicionParaInsertar - 10
		listaCircular[posicionParaInsertar] = datos
		if posicioParaInsertar > final:
			final =  posicioParaInsertar 

	#retorna el los datos del numero de paquete, numeroDePaquete si no se encuentra retorna -1
	def getElemento(int numeroDePaquete)
		posicionABuscar = ((numeroDePaquete - numeroDePaqueteActual) + inicio) - 10#Calculamos la posicion en la que deberia estar ese paquete en el array circular
		dataBytes = listaCircular[posicionABuscar]
		dataBytes = dataBytes[1:3]#Sacamos los bytes donde se encuentra el numero de paquete.
		int.from_bytes(dataBytes, byorder='big')
		if dataBytes == numeroDePaquete:#comparamos que el numero de paquete deseado sea el que se encuentre en la posicion. 
			return listaCircular[posicionABuscar]
		else: 
			return -1

