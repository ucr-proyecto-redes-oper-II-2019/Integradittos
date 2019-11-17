# Construye el grafo de nodos verdes para un nodo naranja a partir del
# archivo csv en la ruta filePath. 
# Retorna un diccionario donde la llave indica el número de un nodo y
# el valor corresponde a la lista de números de los nodos adyacentes.
def OrangeLoadGraph(filePath):
	graphFile = open (filePath, 'r') 
	readLine = graphFile.readline()

	# Diccionario vacío
	graphDictionary = dict()

	while readLine:
		# Separa la línea leída usando comas
		splitLine = readLine.split(",")
		# El nodo actual es el primero en la línea
		currentNode = int(splitLine[0])
		# Los nodos adyacentes son los demás
		adyacentNodes = [int(node) for node in splitLine[1:]]
		# Agrega los datos del nodo actual al diccionario
		graphDictionary[currentNode] =  adyacentNodes

		# Lee la siguiente línea
		readLine = graphFile.readline()

	graphFile.close()

	return graphDictionary

# Carga las IP's de los nodos naranja a partir del archivo csv con ruta filePath.
# Retorna la lista de las IP's en formato de hilera de todos los nodos naranja.
def OrangeLoadOranges(filePath):
	ipFile = open(filePath, 'r')
	ipList = ipFile.read().split(",")

	ipFile.close()

	return ipList
