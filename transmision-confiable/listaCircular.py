
class listaCircular:

	listaCircular = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	inicio = 0 
	final = 0
	numeroDePaqueteActual = 0

	#Se establece la posicion de inicio de la lista que este correspode al RN. 
	def establecerInicio(self, numeroDePaqueteInicio):
		self.numeroDePaqueteActual = numeroDePaqueteInicio		
		self.inicio = numeroDePaqueteInicio % 10

	#Inserta un elemento en la lista, datos(los 516 bytes del paquete) y numeroDePaqueteAInsertar(El numero del paquete que se va a insertar).
	def insertar(self, datos ,numeroDePaqueteAInsertar):#introducimos el nuevoPaquete
		posicionParaInsertar = ((numeroDePaqueteAInsertar - self.numeroDePaqueteActual) + self.inicio) % 10
		self.listaCircular[posicionParaInsertar] = datos#Insertamos los bytes
		if posicionParaInsertar > self.final:
			self.final = posicionParaInsertar

	#retorna el los datos del numero de paquete, numeroDePaquete si no se encuentra retorna -1
	def getElemento(self, numeroDePaquete):
		posicionABuscar = ((numeroDePaquete - self.numeroDePaqueteActual) + self.inicio) % 10#Calculamos la posicion en la que deberia estar ese paquete en el array circular
		dataBytes = self.listaCircular[posicionABuscar]
		if dataBytes == 0:
			return -1
		dataBytes = dataBytes[1:4]#Sacamos los bytes donde se encuentra el numero de paquete.
		dataBytes = int.from_bytes(dataBytes, byteorder='big')
		if dataBytes == numeroDePaquete:#comparamos que el numero de paquete deseado sea el que se encuentre en la posicion. 
			return self.listaCircular[posicionABuscar]#Devolvemos el paquete completo.
		else: 
			return -1

