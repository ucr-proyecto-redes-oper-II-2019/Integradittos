import numpy as np 
#Fabian e Isaa
class listaCirular():

	list listaCircular 
	int inicio = 0 
	int final = 0
	int numeroDePaqueteActual = 0

	def establecerInicio(int nuevoInicio, int numeroDePaquete):#establecemos el nuevo inicio desde nuestra lista.
		inicio = nuevoInicio
		numeroDePaqueteActual = numeroDePaquete

	def insertar(datos ,int numeroDePaqueteAInsertar):#introducimos el nuevoPaquete
		posicionParaInsertar = (numeroDePaquete - numeroDePaqueteActual) + inicio
		posicionParaInsertar = posicionParaInsertar - 10
		listaCircular[posicionParaInsertar] = datos

	def getElemento(int numeroDePaquete)#Obtener un elemento del arreglo, si no se encuentra se retorna un -1
		posicionABuscar = ((numeroDePaquete - numeroDePaqueteActual) + inicio) - 10#Calculamos la posicion en la que deberia estar ese paquete en el array circular
		bytes = listaCircular[posicionABuscar]
		bytes = bytes[1:3]#Sacamos los bytes donde se encuentra el numero de paquete.
		int.from_bytes(bytes, byorder='big')
		if(bytes == numeroDePaquete):#comparamos que el numero de paquete deseado sea el que se encuentre en la posicion. 
			return listaCircular[posicionABuscar]
		else: 
			return -1

