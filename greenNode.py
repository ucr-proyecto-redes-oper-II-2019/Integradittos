# greenNode.py
import random
import threading
from tcpl.tcpl import TCPL # en carpeta inferior
from orangeNode import GreenNodeToken
from greenMessageCodes import GreenMessageCodes
from fileSystem import FileSystem

class GreenNode:
	
	DATA_MAX_SIZE = 1009

	'''
	Constructor de objetos de clase GreenNode.
	Recibe como parametros el numero de puerto del nodo por construir,
	y la IP y puerto del nodo naranja que usa para conectarse.
	'''
	def __init__(self, myPortNumber, orangeIP, orangePortNumber):
		
		self.myPort = myPortNumber
		self.graphID = -1
		
		self.orangeIP = orangeIP
		self.orangePort = orangePortNumber
		
		self.tcpl = TCPL()
		
		# Registros en tabla: nodoDestino [0] | distancia [1] | vecino [2]
		self.neighboursTable = dict()
		# Registros en tabla: ip [0] | puerto [1]
		self.routingTable = dict()
		
		self.fileSystem = FileSystem();

	'''
	Etapa de inicializacion del nodo verde.
	'''
	def _initialization(self):
		# Inicializar servicios basicos
		# Solicitar unirse al grafo
		# Esperar identificacion
		# Construir tabla de enrutamiento
		pass
		
	'''
	Etapa de ejecucion del nodo verde.
	'''
	def _execution(self):
		# Esperar nuevos vecinos (de parte de naranja)
		# Esperar solicitudes de otros verdes
		# Esperar solicitudes de azules
		pass
	
	'''
	Etapa de finalizacion del nodo verde.
	'''
	def _termination(self):
		# Rechazar solicitudes de otros nodos
		# Avisar a un naranja sobre la terminacion
		# Avisar a sus vecinos verdes sobre la finalizacion
		pass
	
	'''
	Ejecuta toda la funcionalidad del nodo verde, incluyendo las etapas
	de inicializacion, ejecucion y terminacion.
	'''
	def run(self):
		self._initialization()
		self._execution()
		self._termination()
	
	''' ### ### ### Solicitudes de azules ### ### ### '''
	
	'''
	Almacenar un archivo.
	'''
	def _putFile(self, requestPack):
		pass
		
	'''
	Recuperar un archivo.
	'''
	def _getFile(self, requestPack):
		pass
	
	'''
	Pregunta si existen fragmentos de un archivo.
	'''
	def _askForFileFragments(self, requestPack):
		pass
	
	'''
	Pregunta si existe un archivo entero.
	'''
	def _askForWholeFile(self, requestPack):
		pass
	
	'''
	Recuperar un archivo.
	'''
	def _getFile(self, requestPack):
		pass
	
	'''
	Localizar un archivo.
	'''
	def _locateFile(self, requestPack):
		pass
	
	'''
	Eliminar un archivo.
	'''
	def _deleteFile(self, requestPack):
		pass
	
	'''
	Migrar un proceso reanudable a otro nodo.
	'''
	def _migrateProcess(self, requestPack):
		pass
	
	'''
	Ejecuta un proceso.
	'''
	def _runProcess(self, requestPack):
		pass
	
	
	''' ### ### ### Transacciones con otros verdes ### ### ### '''
	
	#todo:
	
	'''
	Enviar tabla de enrutamiento a vecinos (actualizar tabla de enrutamiento)
	'''
	def _sendRouteTable(self, routingTable, neighboursTable):

		# Se crea el payload con la tabla, cada registro son 2 bytes
		table = bytearray(1000)
		offset = 0
		for node in routingTable:
			table[offset] = routingTable[node][0] # nodo
			table[offset+1] = routingTable[node][1] # distancia
			offset += 2

		# Se envían los mensajes a los vecinos
		tableMessage = bytearray(DATA_MAX_SIZE)

		# ToDo: Crear encabezado y agregar payload con la tabla
		
		for neighbour in neighboursTable:
			ip = neighboursTable[neighbour][0]
			port = neighboursTable[neighbour][1] 
			tcpl.sendPackage(tableMessage,  port, port)



	'''
	Confirmar que la tabla de enrutamiento está actualizada (tras recibir tabla de enrutamiento)
	'''
	def _checkRouteTable(self, ownTable, receivedTable, sender '''nodo'''):
		items = 0
		offset = 0
		while receivedTable[offset] != 0 and receivedTable[offset+1] != 0:
			items  += 1
			offset += 2
			# Se compraran los datos con nuestra tabla
			# Si ya tenemos la ruta en la tabla checkeamos su distancia
			if receivedTable[offset] in ownTable:
				if receivedTable[offset+1] < ownTable[ receivedTable[offset+1] ][1]:
					# Nueva distancia
					ownTable[ receivedTable[offset+1] ][1] = receivedTable[offset+1] + 1
					# Nuevo nodo vecino (quizá)
					ownTable[ receivedTable[offset+1] ][2] = sender
			else:
				# Si no tenemos esa ruta, la agregamos
				ownTable[ receivedTable[offset] ] = (receivedTable[offset], receivedTable[offset+1], sender)
		print("Recibi una tabla de tamaño: ", items, " del vecino ", sender)



	'''
	Recibir la “presentación” de un nodo verde nuevo.
	Enviar un proceso reanudable.
	Enviar de un segmento de archivo.
	Preguntar por segmentos de un archivo.
	Solicitar el envío de segmentos de un archivo.
	Pedir la eliminación de un archivo o sus fragmentos.
	Avisar sobre terminación de un nodo verde.
	Relocalización de un proceso reanudable
	'''
	
	
	'''
	Actualiza entradas de la tabla de enrutamiento segun nuevos datos
	enviados por un vecino.
	'''
	def updateRoutingTable(self, requestPack):
	
	
	
	''' ### ### ### Solicitudes de naranjas ### ### ### '''
	
	'''
	Agregar un vecino nuevo y presentarse si esta instanciado.
	'''
	def _addNeighbour(self, requestPack):
		pass
	
	
	''' ### ### ### Procedimientos dentro del mismo nodo ### ### ### '''
	
	# todo Acordar estos metodos
	
	#def splitFile(self, fileToSplit):
	#def buildFile(self, fileName):
	#def findFile(self, fileName):
	#def findFragments(self, fileName):
	
