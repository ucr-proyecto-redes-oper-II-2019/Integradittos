# greenNode.py
import random
import threading
import time

from functools import partial
from tcpl.tcpl import TCPL # en carpeta inferior
from orangeNode import GreenNodeToken
from fileSystem import FileSystem
from AssemblePackagesFactory import AssemblePackageFactory
from processSystem import ProcessSystem


class GreenNode:
	''' CÓDIGOS DE MENSAJES '''
	ROUTING_MESSAGE = 80
	GREET_NEIGHBOR = 100
	GREET_NEIGHBOR_ACK = 101
	FILE_EXISTS = 102
	FILE_EXISTS_ACK = 103
	FILE_COMPLETE = 104
	FILE_COMPLETE_ACK = 105
	LOCATE_FILE = 106
	LOCATE_FILE_ACK = 107
	REMOVE_FILE = 108
	REMOVE_FILE_ACK = 109
	PUT_FILE = 110
	PUT_FILE_ACK = 111
	GET_FILE = 112
	GET_FILE_ACK = 113
	EXEC = 114
	EXEC_ACK = 115
	EXEC_STOP = 116
	EXEC_STOP_ACK = 117
	SEND_ROUTE = 118
	SEND_ROUTE_ACK = 119
	CONNECT_ACK = 201

	SEND_PROCESS = 50
	RUN_PROCESS = 51
	ASK_FOR_PROCESS = 52
	PROCESS_OUTPUT = 53
	# ...

	WAITFORACKTIMEOUT = 5
	DATA_MAX_SIZE = 1015
	MAX_RANDOM = 65000
	FILE_NAME_SIZE = 32
	'''  # # #  # # #  # # #  Procedimientos dentro del mismo nodo  # # #  # # #  # # #  '''

	def __init__(self, myPortNumber, orangeIP, orangePortNumber):
		'''
		Constructor de objetos de clase GreenNode.
		Recibe como parametros el numero de puerto del nodo por construir,
		y la IP y puerto del nodo naranja que usa para conectarse.
		Incluye la etapa de inicialización del nodo verde.
		'''
		# Inicializar servicios basicos
		self.myPort = myPortNumber
		self.myID = -1

		self.orangeIP = orangeIP
		self.orangePort = orangePortNumber

		self.tcpl = TCPL()

		self.tcpl.startService(self.myPort)
		self.processSystem = ProcessSystem(self.myPort , True)

		# Diccionario con GreenNodeToken
		self.neighboursTable = dict()
		# Registros en tabla: nodoDestino [0] | distancia [1] | vecino [2]
		self.routingTable = dict()

		self.fileSystem = FileSystem(self.myPort)

		self.assemblePackage = AssemblePackageFactory()

		# Solicitar unirse al grafo
		# Esperar identificacion

	def _execution(self):
		'''
		Etapa de ejecucion del nodo verde.
		'''
		self.isRunning = True
		# Esperar nuevos vecinos (de parte de naranja)
		paquete = self.assemblePackage.assemblePackageConnect()
		#Si logra enviar su paquete connect puede empezar a escuchar request.
		if(self.tcpl.sendPackage(paquete, self.orangeIP, self.orangePort)):
			package, address = self.tcpl.receivePackage()
			requestNumber, beginConfirmationAnswer, serviceNumber, sizeBodyPriority, ttl, fuente, destino,  data = self.assemblePackage.unpackPackage(package)
			self.myID = int.from_bytes(data[0:2], byteorder='big')
			threadReceiving = threading.Thread(target = self._receiveMessages)
			threadRouting = threading.Thread(target = self._routingThread)
			threadRouting.start()
			threadReceiving.start()
		else:
			print("No fue posible enviar el paquete para solicitar ID al nodo Naranja")
			return -1
	def _termination(self):
		'''
		Etapa de finalizacion del nodo verde.
		'''
		# Rechazar solicitudes de otros nodos
		# Avisar a un naranja sobre la terminacion
		# Avisar a sus vecinos verdes sobre la finalizacion
		pass

	def run(self):
		'''
		Ejecuta toda la funcionalidad del nodo verde, incluyendo las etapas
		de ejecucion y ,terminacion.
		'''
		self._execution()
		self._termination()


	def _extractPortAndIp(self, data):
		''' la informacion
		:return: retorna el numero de puerto y la ip.
		'''
		ip = ""
		ip += str(data[0]) + "."
		ip += str(data[1]) + "."
		ip += str(data[2]) + "."
		ip += str(data[3])
		port = str(int.from_bytes(data[4:6], byteorder='big'))
		return port, ip

	def _receiveMessages(self):
		'''
		Recibe constantemente mensajes de otros nodos, y los atiende
		si son solicitudes para el nodo actual.
		'''
		while self.isRunning:
			#print("Estoy recibiendo mensajes.")
			package, address = self.tcpl.receivePackage()
			# Si es el nodo destino se ruteo
			destination = int.from_bytes(package[13:15], byteorder='big')
			#Si el ID destino del mensaje no coincide con el mio entonces tengo que rutearlo.
			if destination != self.myID and destination != 0:
				if destination in self.routingTable:
					ip = self.neighboursTable[ self.routingTable[destination][2] ].ip
					port = self.neighboursTable[ self.routingTable[destination][2] ].port
					print ("Ruteando paquete hacia ", destination, " por vecino: ", self.routingTable[destination][2], ip, port )
					self.tcpl.sendPackage(package, ip, port)
				else:
					print ("Mensaje hacia nodo: ", destination, " desechado, no hay entrada en la tabla de ruteo.")
			else:
				hiloDeAtencionRequest = threading.Thread(target=self._attendRequests, args=(package, address))
				hiloDeAtencionRequest.start()

	def sendGreetNeighbor(self, indice):
		'''
			Subrutina que se encarga de saludar a los vecinos de los que se tienen conocimiento de que estan instanciados.
		'''
		if self.neighboursTable.get(indice).ip != "0.0.0.0":
			package = self.assemblePackage.assemblePackageGreetNeighbor(self.myID, self.myID, self.neighboursTable.get(indice).id)
			self.tcpl.sendPackage(package, self.neighboursTable.get(indice).ip, self.neighboursTable.get(indice).port)
		pass


	def _attendRequests(self, package, ipPort):
		'''
		Atiende una solicitud hecha al nodo actual.
		'''
		requestNumber, beginConfirmationAnswer, serviceNumber, sizeBodyPriority, ttl, fuente, destino, data = self.assemblePackage.unpackPackage(package)

		if serviceNumber == self.CONNECT_ACK: #Se reciben los vecio
		   self._connect(beginConfirmationAnswer, data)

		elif serviceNumber == self.GREET_NEIGHBOR: #Se me informa que tengo un vecino
			print("Mi vecino me saludo y tiene la direccion: ", ipPort)
			self._greetNeighbor(requestNumber, beginConfirmationAnswer, ipPort)
			self.imprimirListVecinos()

		elif serviceNumber == self.GREET_NEIGHBOR_ACK: # recibo un ack de que mi vecino ya sabe que existo
			pass

		elif serviceNumber == self.SEND_ROUTE: #Se me envia la tabla de enrutamiento.
			self._checkRouteTable(data, fuente)

		elif serviceNumber == self.SEND_ROUTE_ACK: #Se me indica que la tabla que mande se recibio correctamente.
			pass

		elif serviceNumber == self.FILE_EXISTS: #Recibo un mensaje de pregunta si un archivo existe
			self._fileExistInSelf(requestNumber, data, ipPort)
			pass

		elif serviceNumber == self.FILE_EXISTS_ACK: #Se medio una respuesta acerca de la existencia de un archivo.
			pass

		elif serviceNumber == self.FILE_COMPLETE: #Se me pregunta si un archivo x(viene en los datos) esta completo
			pass
		elif serviceNumber == self.LOCATE_FILE: #Se me pregunta por la lista de nodos que tiene x archivo
			pass
		elif serviceNumber == self.LOCATE_FILE_ACK:  # Respuesta con una lista de ids que contienen el archivo.
			pass
		elif serviceNumber == self.REMOVE_FILE:  # Se me indica que debo borrar X archivo de mi almacenamiento
			#self.removeFile(requestNumber)
			pass
		elif serviceNumber == self.REMOVE_FILE_ACK:  # Respuesta de que un archivo pudo ser borrado.
			pass
		elif serviceNumber == self.PUT_FILE:  # Se me indica que debo almacenar x archivo.
			pass
		elif serviceNumber == self.PUT_FILE_ACK: #Se me contesta acerca de si se guardo el archivo.
			pass
		elif serviceNumber == self.GET_FILE: #Se me solicita y fragmento de x archivo.
			pass
		elif serviceNumber == self.GET_FILE_ACK: #Se me da Y fragmento de x archivo que solicite.
			pass
		elif serviceNumber == self.EXEC: # Se me indica que debo correr un proceso.
			pass
		elif serviceNumber == self.SEND_PROCESS:
			print ("Recibi una solicitud para recibir proceso.")
			# Acá se pueden poner condiciones para recibir el proceso o no
			if True:
				answer = bytearray(package)
				# Activamos trans conf por medio del sistema de procesos
				receiveProcessThread = threading.Thread(target=self._receiveProcess, args=(bytes(package),))
				receiveProcessThread.start()
				# Aceptamos la solicitud
				answer[15] = 1
			else:
				# Denegamos la solicitud
				answer[15] = 0
			self.tcpl.sendPackage(answer, ipPort[0], ipPort[1])
		elif serviceNumber == self.RUN_PROCESS:
			print ("Recibi una solicitud para correr proceso:", package[15:75].decode(), ".")
			runProcessThread = threading.Thread(target=self._runProcess, args=(bytes(package),))
			runProcessThread.start()
			self.tcpl.sendPackage(package, ipPort[0], ipPort[1])
		elif serviceNumber == self.ASK_FOR_PROCESS:
			procName = package[15:75].decode().strip('\x00')
			print("Se me consultó el estado del proceso:", procName, ".")
			answer = bytearray(package)
			state = self.processSystem.isProcessDone(str(procName))
			answer[15] = state
			# Enviamos la respuesta
			print("El proceso:", procName, "está en estado", state, ".")
			self.tcpl.sendPackage(answer, ipPort[0], ipPort[1])




	'''  # # #  # # #  # # #  Solicitudes de azules  # # #  # # #  # # #  '''

	def _receiveProcess(self, requestPack):
		'''
		Recibe un proceso de un nodo azul.
		'''
		program = requestPack[15:75].decode('utf-8').strip('\x00')
		executable = requestPack[75:125].decode('utf-8').strip('\x00')
		print("Proceso:", program, ", ejecutable:", executable)
		# Recibimos el archivo por trans confiable
		self.processSystem.receiveProcess(program, executable, self.myPort)

	def _migrateProcess(self, requestPack):
		'''
		Migrar un proces 3 en la lista de adyacencias
	o reanudable a otro nodo.
		'''
		pass

	def _runProcess(self, requestPack):
		'''
		Ejecutar un proceso.
		'''
		program = requestPack[15:75].decode('utf-8').strip('\x00')
		self.processSystem.executeProcess(program)



	'''  # # #  # # #  # # #  Transacciones con otros verdes  # # #  # # #  # # #  '''


	def _greetNeighbor(self, requestNumber, beginConfirmationAnswer, ipPort):
		'''
		Envía un mensaje saludando a un vecino instanciado.
		'''
		self.neighboursTable[beginConfirmationAnswer].ip = ipPort[0]
		self.neighboursTable[beginConfirmationAnswer].port = ipPort[1]
		self.neighboursTable[beginConfirmationAnswer].state = True
		package = self.assemblePackage.assemblePackageGreetNeighborACK(requestNumber, self.myID, self.neighboursTable.get(beginConfirmationAnswer).id)
		self.tcpl.sendPackage(package, ipPort[0], ipPort[1])

	def _routingThread(self):
		#Hilo que se va a encargar de enviar la tabla de ruteo cada 1 segundo.
		while(1):
			print("Esoty enviando la tabla de enrutamiento")
			self.imprimirTablaDeEnrutamiento()
			self._sendRouteTable()
			time.sleep(25)

	def _sendRouteTable(self):
		'''
		Enviar tabla de enrutamiento a vecinos (actualizar tabla de enrutamiento)
		'''
		routingTable = self.routingTable
		neighboursTable = self.neighboursTable

		# Se crea el payload con la tabla, cada registro son 2 bytes
		table = bytearray(1000)
		offset = 0
		for node in routingTable:
			table[offset:(offset+2)] = routingTable[node][0].to_bytes(2, byteorder='big') # nodo
			table[(offset+2):(offset+4)] = routingTable[node][1].to_bytes(2, byteorder='big') # distancia
			offset += 4

		# Se envían los mensajes a los vecinos
		tableMessage = bytearray(self.DATA_MAX_SIZE)
		# ToDo: Agregar código de enviar la tabla
		tableMessage[4:6] = bytearray(2)  # 0
		tableMessage[6] = self.SEND_ROUTE
		tableMessage[7:9] = bytearray(2)  # sin prioridad
		tableMessage[9:11] = int(50).to_bytes(2, byteorder='big')
		tableMessage[15:] = table
		# ...

		for neighbour in neighboursTable:
			# fuente - destino
			if neighboursTable[neighbour].state is True :
				tableMessage[0:4] = random.randrange(self.MAX_RANDOM).to_bytes(4, byteorder='big')
				tableMessage[11:13] = int(self.myID).to_bytes(2, byteorder='big')
				tableMessage[13:15] = int(neighbour).to_bytes(2, byteorder='big')
				ip = neighboursTable[neighbour].ip
				port = neighboursTable[neighbour].port
				self.tcpl.sendPackage(tableMessage, ip, port)

	def _checkRouteTable(self, receivedTable, sender):
		'''
		Confirmar que la tabla de enrutamiento está actualizada (tras recibir tabla de enrutamiento)
		'''
		ownTable = self.routingTable
		items = 0
		offset = 0
		while int.from_bytes(receivedTable[offset:offset+2], byteorder='big') != 0:
			items  += 1

			# 2 bytes de nodo + 2 bytes de distancia = 4 bytes
			nodeNum = int.from_bytes(receivedTable[offset:offset+2], byteorder='big')
			distance = int.from_bytes(receivedTable[offset+2:offset+4], byteorder='big')

			# Se compraran los datos con nuestra tabla
			# Si ya tenemos la ruta en la tabla checkeamos su distancia
			if nodeNum in ownTable:
				if int.from_bytes(receivedTable[offset+2:offset+4], byteorder='big') < ownTable[ nodeNum ][1]:
					# Nueva distancia
					ownTable[ nodeNum ][1] = distance + 1
					# Nuevo nodo enlace (quizá)
					ownTable[ nodeNum ][2] = sender
			else:
				# Si no tenemos esa ruta, la agregamos
				ownTable[ nodeNum ] = [nodeNum, distance+1, sender]

			offset += 4
		#print("Recibi una tabla de tamaño: ", items, " del vecino ", sender)

	def _receiveRelocatedProcess(self, package):
		'''
		Recibir un proceso reanudable.
		'''
		pass

	def _updateRoutingTable(self, requestPack):
		'''
		Actualiza entradas de la tabla de enrutamiento segun nuevos datos
		enviados por un vecino.
		'''
		pass

	def imprimirListVecinos(self):
		diccionario = self.neighboursTable.copy()
		print("Mi numero de ID es: ", self.myID, " Y la tabla de adyacencias")
		for i in diccionario:
			print("ID: ", diccionario.get(i).id)
			print("Ip: ", diccionario.get(i).ip)
			print("Puerto: ", diccionario.get(i).port)
			print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
		print("--------------------------Aqui termina la tabla de adyacencias-----------------------")


	'''  # # #  # # #  # # #  Solicitudes de/ a naranjas  # # #  # # #  # # #  '''

	'''
	Agregar un vecino nuevo y presentarse si esta instanciado.
	'''
	def _addNeighbour(self, requestPack):
		# Agregar a tabla de vecinos
		# Presentarse al vecino si está instanciado
		pass

	def _connect(self, beginConfirmationAnswer, data):
		'''
		Se recibe la respuesta de un connect y se añade su id propio y el de sus vecinos con sus respectivas IPs si estan instanciados.
		:param beginConfirmationAnswer:
		:param data:
		:return:
		'''
		neighbourID = int.from_bytes(data[0:2], byteorder='big')
		# El primer mensaje que se envia es su ID. Asi que revisamos que este mensaje no sea el primero para añadirlo en la lista de adyacencias.
		if (beginConfirmationAnswer != neighbourID):
			neighbourNode = GreenNodeToken(neighbourID)
			port, ip = self._extractPortAndIp(data[2:8])
			# Si viene una IP validad en el paquete debemos proceder añadirla a la lista y saludar, de lo contrario no se añade ninguna IP.
			if ip != "0.0.0.0":
				neighbourNode.ip = ip
				neighbourNode.port = port
				neighbourNode.state = True
				self.neighboursTable[neighbourID] = neighbourNode
				self.sendGreetNeighbor(neighbourID)
			else:
				self.neighboursTable[neighbourID] = neighbourNode
			# Siempre añadimos a nuestra tabla de ruteo al vecino aunque no este instanciado.
			arrayTable = [neighbourID, 1, neighbourID]
			self.routingTable[neighbourID] = arrayTable
			self.imprimirListVecinos()
		else:  # Guardamos cual es nuestro ID.
			self.myID = beginConfirmationAnswer

	def imprimirTablaDeEnrutamiento(self):
		tabla = self.routingTable
		print("Esta es la tabla de enrutamiento actual: ")
		for indice  in tabla:
			print (tabla[indice])
		print("-------------------------------------------Final Tabla enrutamiento--------------------------------------------")
