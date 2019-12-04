# greenNode.py
import random
import threading
from tcpl.tcpl import TCPL # en carpeta inferior
from orangeNode import GreenNodeToken
from greenMessageCodes import GreenMessageCodes
from fileSystem import FileSystem

class GreenNode:

	FILE_FRAGMENT_MAX_SIZE = 1000
	
	'''
	Constructor de objetos de clase GreenNode.
	Recibe como parametros el numero de puerto del nodo por construir,
	y la IP y puerto del nodo naranja que usa para conectarse.
	Incluye la etapa de inicialización del nodo verde.
	'''
	def __init__(self, myPortNumber, orangeIP, orangePortNumber):
		# Inicializar servicios basicos
		self.myPort = myPortNumber
		self.graphID = -1
		
		self.orangeIP = orangeIP
		self.orangePort = orangePortNumber
		
		self.tcpl = TCPL()
		
		self.neighboursTable = []
		self.routingTable = []
		
		self.fileSystem = FileSystem(str(myPortNumber))
		
		# Solicitar unirse al grafo
		# Esperar identificacion
		
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
		self._execution()
		self._termination()
	
	'''  # # #  # # #  # # #  Solicitudes de azules  # # #  # # #  # # #  '''
	
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
	
	
	'''  # # #  # # #  # # #  Transacciones con otros verdes  # # #  # # #  # # #  '''
	
	#todo:
	'''
	Enviar una nueva ruta más corta hacia uno de los nodos (actualizar tabla de enrutamiento)
	def _sendRoutingTableUpdate(self):
	def _updateRoutingTable(self, package):

	Recibir la “presentación” de un nodo verde nuevo.
	def _sendNeighbourIndtroduction(self, neighbour):
	def _receiveNeighbourIntroduction(self, package):

	Relocalizar un proceso reanudable.
	def _relocateProcess(self, process):
	def _receiveRelocatedProcess(self, package):

	Enviar un segmento de archivo.
	def _sendFileFragment(self, fragment):
	def _receiveFileFragment(self, package):

	Preguntar por segmentos de un archivo.
	def _askForFragments(self, fileName):
	def _findFragments(self, package):

	Solicitar el envío de segmentos de un archivo.
	def _retrieveFragments(self, fileName):
	def _findAndSendFragments(self, package):

	Pedir la eliminación de un archivo o sus fragmentos.
	def _reqestFileDeletion(self, fileName):
	def _deleteFileRequested(self, package):

	Avisar sobre terminación de un nodo verde.
	def _tellAboutTermination(self):
	def _updateRoutingTableAfterTermination(self, package):
	'''
	
	'''
	Actualiza entradas de la tabla de enrutamiento segun nuevos datos
	enviados por un vecino.
	'''
	def _updateRoutingTable(self, requestPack):
		pass
	
	
	'''  # # #  # # #  # # #  Solicitudes de/ a naranjas  # # #  # # #  # # #  '''
	
	'''
	Agregar un vecino nuevo y presentarse si esta instanciado.
	'''
	def _addNeighbour(self, requestPack):
		pass
	
	
	''' ### ### ### Procedimientos dentro del mismo nodo ### ### ### '''

	#def splitFile(self, fileToSplit):
	#def buildFile(self, fileName):
	
