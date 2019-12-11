# greenNode.py
import random
import threading
from tcpl.tcpl import TCPL # en carpeta inferior
from orangeNode import GreenNodeToken
from greenMessageCodes import GreenMessageCodes
from fileSystem import FileSystem

class GreenNode:
	
	DATA_MAX_SIZE = 1009
	MAX_RANDOM = 65000
	
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
		
		# Registros en tabla: ip [0] | puerto [1]
		self.neighboursTable = dict()
		# Registros en tabla: nodoDestino [0] | distancia [1] | vecino [2]
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
		self.tcplService.startService(self.myPort)
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
	def _sendRouteTable(self):
		routingTable = self.routingTable
		neighboursTable = self.neighboursTable
		
		# Se crea el payload con la tabla, cada registro son 2 bytes
		table = bytearray(1000)
		offset = 0
		for node in routingTable:
			table[offset] = routingTable[node][0].to_bytes(2, byteorder='big') # nodo
			table[offset+2] = routingTable[node][1].to_bytes(2, byteorder='big') # distancia
			offset += 4

		# Se envían los mensajes a los vecinos
		tableMessage = bytearray(DATA_MAX_SIZE)

		# ToDo: Agregar código de enviar la tabla
		tableMessage[0:4] = random.randrange(MAX_RANDOM)
		tableMessage[4:6] = 0
		# tableMessage[6] = código
		tableMessage[7:9] = 0 # sin prioridad
		# ...
		
		for neighbour in neighboursTable:
			ip = neighboursTable[neighbour][0]
			port = neighboursTable[neighbour][1] 
			tcpl.sendPackage(tableMessage,  port, port)

	'''
	Confirmar que la tabla de enrutamiento está actualizada (tras recibir tabla de enrutamiento)
	'''
	def _checkRouteTable(self, receivedTable, sender '''nodo'''):
		ownTable = self.routingTable

		items = 0
		offset = 0
		while receivedTable[offset] != 0 and receivedTable[offset+2] != 0:
			items  += 1
			
			# 2 bytes de nodo + 2 bytes de distancia = 4 bytes
			nodeNum = int.from_bytes(receivedTable[offset:offset+2], byteorder='big')
			distance = int.from_bytes(receivedTable[offset+2:offset+4], byteorder='big')
			
			# Se compraran los datos con nuestra tabla
			# Si ya tenemos la ruta en la tabla checkeamos su distancia
			if nodeNum in ownTable:
				if receivedTable[offset+2] < ownTable[ nodeNum ][1]:
					# Nueva distancia
					ownTable[ nodeNum ][1] = distance + 1
					# Nuevo nodo enlace (quizá)
					ownTable[ nodeNum ][2] = sender
			else:
				# Si no tenemos esa ruta, la agregamos
				ownTable[ nodeNum ] = [nodeNum, distance, sender]
				
			offset += 4
		print("Recibi una tabla de tamaño: ", items, " del vecino ", sender)

	
	'''
	Recibir mensajes
	'''
	 def receiveMessages(self): 
        while 1:
            #print("Estoy recibiendo mensajes.")
            package, address = self.tcplService.receivePackage()
            # Si es el nodo destino se ruteo
            destinationNode = int.from_bytes(package[13:15], byteorder='big')
            if destination != self.graphID:
				if destination in self.routingTable:
					ip = self.neighboursTable[ self.routingTable[destination][2] ].ip
					port = self.neighboursTable[ self.routingTable[destination][2] ].port
					print ("Ruteando paquete hacia ", destination, " por vecino: ", self.routingTable[destination][2], ip, port )
					self.tcplService.sendPackage(package, ip, port)
				else:
					print ("Mensaje hacia nodo: ", destination, " desechado, no hay entrada en la tabla de ruteo.")
			else:
				hiloDeAtencionRequest = threading.Thread(target=self.attendRequests, args=(package, address))
				hiloDeAtencionRequest.start()
        pass
     
    
    def _attendRequests(self, package, ipPort):
		pass
	
	

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
	
