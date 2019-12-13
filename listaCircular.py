
class listaCircular:
	TAMANO_LISTA = 10
	INICIO_METADATOS = 1
	FIN_METADATOS = 4
	lista_circular = [] #= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	inicio = 0
	final = 0
	numero_de_paquete_actual = 0
	def __init__(self):
		for i in range(self.TAMANO_LISTA):
			self.lista_circular += [0]

	# Se establece la posicion de inicio de la lista que este correspode al RN.
	def establecer_inicio(self, numero_de_paquete_inicio):
		self.numero_de_paquete_actual = numero_de_paquete_inicio
		self.inicio = numero_de_paquete_inicio % self.TAMANO_LISTA


	# Inserta un elemento en la lista, datos(los 516 bytes del paquete)
	# y numeroDePaqueteAInsertar(El numero del paquete que se va a insertar).
	def insertar(self, datos, numero_de_paquete_a_insertar): # introducimos el nuevoPaquete
		posicion_para_insertar = ((numero_de_paquete_a_insertar - self.numero_de_paquete_actual) + self.inicio) % self.TAMANO_LISTA
		self.lista_circular[posicion_para_insertar] = datos # Insertamos los bytes
		if posicion_para_insertar > self.final:
			self.final = posicion_para_insertar

	# retorna el los datos del numero de paquete, numeroDePaquete si no se encuentra retorna -1
	def get_elemento(self, numero_de_paquete):
		posicion_a_buscar = ((numero_de_paquete - self.numero_de_paquete_actual) + self.inicio) % self.TAMANO_LISTA # Calculamos la posicion en la que deberia estar ese paquete en el array circular
		data_bytes = self.lista_circular[posicion_a_buscar]
		if data_bytes == 0:
			return -1
		data_bytes = data_bytes[self.INICIO_METADATOS:self.FIN_METADATOS] # Sacamos los bytes donde se encuentra el numero de paquete.
		data_bytes = int.from_bytes(data_bytes, byteorder='big')
		if data_bytes == numero_de_paquete: # comparamos que el numero de paquete deseado sea el que se encuentre en la posicion.
			return self.lista_circular[posicion_a_buscar] # Devolvemos el paquete completo.
		else:
			return -1

