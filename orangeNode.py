import threading

from AssemblePackagesFactory import AssemblePackageFactory
import tcpl.tcpl # en carpeta inferior

# Objeto usado para representar los nodos verdes en la lista de adyancencia
class GreenNodeToken:

	def __init__(self, id, ip = 0, port = 0, state = False):
		self.id = id
		self.ip = ip
		self.port = port
		self.state = state


class OrangeNode:

	DATA_MAX_SIZE = 1009

	def __init__(self, id):
		self.id = id
		# Estas listas deberían ser atrributos de instancia
		self.freeNodeList = []
		self.orangeNodesList = []
		self.graphDictionary = dict()
		self.tcplService = tcpl.TCPL()

	# Inicia el nodo, creando hilos e iniciando objetos/estructuras necesarias

	# ToDo: TCPL requiere su propio hilo
	def start(self):
		tcplThread = threading.Thread(target=self.tcpL.startService())
		tcplThread.start()
		self.loadOrangeNeighboring("")

		pass

	# Construye el grafo de nodos verdes para un nodo naranja a partir del
	# archivo csv en la ruta filePath. 
	# Retorna un diccionario donde la llave indica el número de un nodo y
	# el valor corresponde a la lista de números de los nodos adyacentes.

	# ToDo: crear una subrutina o implementar en el cosntructor que se llame esta
	# subrutina para cargar el grafo, asì como llenar la lista dde nodos verdes libres
	# freeNodeList()
	def loadGreenGraph(filePath):
		graphFile = open(filePath, 'r')
		readLine = graphFile.readline()

		# Diccionario vacío
		graphDictionary = dict()
		while readLine:
			# Separa la línea leída usando comas
			splitLine = readLine.split(",")
			# El nodo actual es el primero en la línea
			currentNodeId = int(splitLine[0])
			# Creamos una lista de nodo/vecinos para cada nodo
			graphDictionary[currentNodeId] = list()
			# El primero de la lista que precede a sus vecinos
			graphDictionary[currentNodeId].append( GreenNodeToken(currentNodeId))
			# Los nodos adyacentes son los demás
			adyacentNodes = list()
			for nodeId in splitLine[1:]:
				adyacentNodes.append( GreenNodeToken(nodeId) )
			# Agregar lista de vecinos a la cabeza de la lista
			graphDictionary[currentNodeId].extent(adyacentNodes)

			# Lee la siguiente línea
			readLine = graphFile.readline()

		graphFile.close()

		return graphDictionary

	# Carga las IP's de los nodos naranja a partir del archivo csv con ruta filePath.
	# Retorna la lista de las IP's en formato de hilera de todos los nodos naranja.

	# Nota: ¿¿¿Acá no faltaria algo como tuplas id/ip:puerto para los naranjas???
	def loadOranges(filePath):
		ipFile = open(filePath, 'r')
		ipList = ipFile.read().split(",")

		ipFile.close()

		return ipList

	def loadOrangeNeighboring(self, orangeNodes):
		listOrangeNodes = []
		listaDeIpsYpuertos = orangeNodes.split()
		for i in range(0, len(listaDeIpsYpuertos), 2):
			listOrangeNodes.append([listaDeIpsYpuertos[i], listaDeIpsYpuertos[i + 1]])
		return listOrangeNodes
	
	''' INTERFACE '''

	def checkNodeNumber(self, nodeNumber):
		"""Si devuelve un True es que el nodo ya ha sido instanciado. """
		listaNodosVerdes = self.graphDictionary.get(nodeNumber)
		return listaNodosVerdes[0].state


	def instantiateNode(self, numeroDeNodo, ip, port):
		listaNodosVerdes = self.graphDictionary.get(numeroDeNodo)
		listaNodosVerdes[0].ip = ip
		listaNodosVerdes[0].port = port
		listaNodosVerdes[0].state = True
		pass

	# Subrutina que atiende requests y actúa según la que recibe
	# Debe correr en otro hilo
	def attendRequests(self):

		pass

	# Envía el nombre a un nodo verde cuándo se logró ser instanciado, además de su
	# lista de vecinos
	def sendGreenInfo(self):

		pass


	# ... subrutinas que sean necesarias para envío de mensajes (usando TCPL)
	# como: 
	# -preguntar si un nodo ha sido instanciado (REQUEST_POS)
	# -reportar si un nodo está instanciado o no (REQUEST_POS_ACK)
	# -anunciar una instanciación (CONFIRM_POS)
	# -confirmar una instanciación (CONFIRM_POS_ACK)
	#
	# OJO: HAY UN THREAD RESPONSABLE DE RECIBIR TODAS LAS SOLICITUDES, ENTONCES, SI
	# POR EJEMPLO SE ENVÍO UN REQUEST_POS A TODOS LOS NARANJAS, EL CONTROL DE QUE 
	# SE RECIBA LA RESPUESTA DE TODOS LOS NARANJAS SE DEBE HACER POR MEDIO DE LISTAS
	# INTERNAS DEL NODO NARANJA (teniendo cuidado con que si no hay respuesta de un nodo
	# naranja, puede que este no este arriba)
