import csv
#import greenNode # estructura que representa un nodo verde en el grafo

# Esta clase lee/escribe CSVs relacionados con los nodos verdes del grafo
class CSVPaser:

	#__init__(self):

	# Recibe la ruta del archivo csv que contiene los nodos verdes y sus vecinos
	# y retorna la lista de adyacencia del grafo
	def readGreenNodeGraph(self, filePath):
		adjacencyList = [][]
		# Se abre el csv
		with open(filePath, mode='r') as csvFile:
    		csvGreenGraph = csv.writer(csvFile, delimiter=',')
			# Para cada fila en el archivo csv
			for row in greenGraph:
				# Obtenemos la lista de nombre, vecino1, vecino2 ...
				nodeList = split(row)
				greenNode = greenNode.GreenNode(nodeList[1])
				for neighbour in range(1, len(nodeList)):
					# ToDo: terminar implementación de creación de lista de adyaciencia
				

	def writeCSV(self, greenNodeList):
