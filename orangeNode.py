# coding=utf-8
import random
import threading
from TxtReader import TxtReader
from AssemblePackagesFactory import AssemblePackageFactory
from tcpl.tcpl import TCPL # en carpeta inferior
import time 
# Objeto usado para representar los nodos verdes en la lista de adyancencia
class GreenNodeToken:

    def __init__(self, id, ip = 0, port = 0, state = False):
        self.id = id
        self.ip = ip
        self.port = port
        self.state = state

class OrangeNode:
    # deberia ser un atributo de instancia (ver constructor)
    #PUERTO = "6666"
    DATA_MAX_SIZE = 1009
    POSNUMEROSERVICIO = 6
    CONNECT = 200

    REQUESTPOS = 205
    REQUESTPOSACK = 206
    CONFIRMPOS = 210
    CONFIRMPOSACK = 211
    DISCONNECT = 216
    DISCONNECTACK = 220
    REMOVE = 220
    REMOVEACK = 221
    WAITFORACKDELAY = 1
    WAITFORACKTIMEOUT = 5

    def __init__(self, id, ip, port):
        self.adyacentNodes = dict()
        self.id = id
        self.tcplService = TCPL()
        # Estas listas deberían ser atrributos de instancia
        self.freeNodeList = []
        self.orangeNodesList = []
        # Lista de nombres de nodos esperando por ser instanciados
        self.instantiatingList = []
        self.localIp = ip
        self.localPort = port
        self.assemblePackage = AssemblePackageFactory()

        ''' Lista (dict) utilizada para llevar registro de cuáles solicitudes
         naranja - naranja han sido confirmadas, por ejemplo, aumentar
         la entrada [546] de la solicitud REQUESTPOS con ese mismo número
        cuando se reciba un REQUESTPOSACK '''
        self.confirmationCounters = dict()


    # Inicia el nodo, creando hilos e iniciando objetos/estructuras necesarias

    # ToDo: TCPL requiere su propio hilo
    def start(self, csvPath, orangesPath):
        #1 debe cargar lista de nodos naranjas.
        #2 cargamos el grafo verde. 
        #3 Empezamos tcpl para que escuche solicitudes
        #4 Empezamos un hilo que retire mensajes de la bolsa de tcpl y atienda solicutes. 
        #
        ruta = orangesPath
        textReader = TxtReader()
        self.loadOrangeNeighboring(textReader.readTxt(ruta))
        self.adyacentNodes = self.loadGreenGraph(csvPath)
        #self.freeNodeList.append(1)
        #self.freeNodeList.append(72)
        self.tcplService.startService(self.localPort)
        threadReceiving = threading.Thread(target = self.popPackage())
        threadReceiving.start() #



        ''' esto es en otra subrutina
        while 1:
            package = self.popPackage() '''

        pass

    ''' Construye el grafo de nodos verdes para un nodo naranja a partir del
    archivo csv en la ruta filePath.
    Retorna un diccionario donde la llave indica el número de un nodo y
    el valor corresponde a la lista de números de los nodos adyacentes.
    ToDo: crear una subrutina o implementar en el cosntructor que se llame esta
    subrutina para cargar el grafo, asì como llenar la lista dde nodos verdes libres
    freeNodeList() '''
    def loadGreenGraph(self, filePath):
        
        ''' NEWER VERSION:
        graphFile = open (filePath, 'r') 
		reader = csv.reader(graphFile)
		
		# Diccionario vacío
		graphDictionary = dict()
		
		# Build dictionary
		for row in reader:
			graphDictionary[row[0]] = row[1:]
		
		readLine = graphFile.readline()

		graphFile.close()
		return graphDictionary
        '''

        graphFile = open (filePath, 'r')
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
            graphDictionary[currentNodeId].append( GreenNodeToken(currentNodeId) )
            # Los nodos adyacentes son los demás
            adyacentNodes = list()
            for nodeId in splitLine[1:]:
                adyacentNodes.append( GreenNodeToken(int(nodeId)) )
            # Agregar lista de vecinos a la cabeza de la lista
            graphDictionary[currentNodeId].extend(adyacentNodes)

            # Lee la siguiente línea
            readLine = graphFile.readline()
            self.freeNodeList.append(currentNodeId)
        graphFile.close()

        return graphDictionary



    ''' INTERFACE '''

    def checkNodeNumber(self, nodeNumber):
        """Si devuelve un True es que el nodo ya ha sido instanciado. """
        #self.lis
        pass

    def instantiateNode(self, numeroDeNodo, ip, port):
        self.adyacentNodes.get(numeroDeNodo)[0].ip = ip
        self.adyacentNodes.get(numeroDeNodo)[0].port = port
        self.adyacentNodes.get(numeroDeNodo)[0].state = True
        print("Instancié el nodo:", numeroDeNodo, "en la lista de adyacencias")
        self.printAdyacencyList(self.adyacentNodes)
    # Subrutina que atiende requests y actúa según la que recibe


    # Envía el nombre a un nodo verde cuándo se logró ser instanciado, además de su
    # lista de vecinos
    def sendGreenInfo(self):
        pass
    #Bug nunca envia el confirmPosAck
    def attendRequests(self, package, ipPort):
        numeroDeRequest, inicioConfirmacionRespuesta, numeroDeServicio, tamCuerpoPrioridad, datos = self.assemblePackage.unpackPackage(package)
        #print(numeroDeRequest, inicioConfirmacionRespuesta, numeroDeServicio, tamCuerpoPrioridad, ipPort, "\n")
        ''' Para REQUESTPOS es mas facil si la subrutina genera el número de nodo las veces
        que sean necesarias y retorna la instanciada. Por esto no estara "position" como parámetro de la 
        funcion. '''
        ipFuente, puertoFuente = ipPort
        if numeroDeServicio == self.REQUESTPOS:
            #print("Este es el numero de de tamaño cuerpo prioridad", tamCuerpoPrioridad)
            print("Recibí un request pos de:", tamCuerpoPrioridad)
            #Si es un request service se debe sacar un nodo verde no instanciado
            #preguntar a los demas si no lo tienen instancido
            self.requestPosACK(inicioConfirmacionRespuesta, ipPort, package)

        elif numeroDeServicio == self.REQUESTPOSACK:
            #Confirma que un id de nodo verde no esta usado.
            #Algun tipo de contador para cuando reciba los
            if inicioConfirmacionRespuesta == 1:
                self.confirmationCounters[numeroDeRequest] += 1 #Aumentamos el contador de request ack recibidos.
            else: #Nota para los programadores: Esto nunca esta pasando, ya que antes habian un remove y como era un diccionario debia caerse.
                if numeroDeRequest in self.confirmationCounters:
                    self.confirmationCounters.pop(numeroDeRequest)
                    #print(self.instantiatingList)
                    #self.instantiatingList.remove(inicioConfirmacionRespuesta)

        elif numeroDeServicio == self.CONFIRMPOS:
            #Debe armar un corfirm pos ack
            #print("Recibí un request pos de:", tamCuerpoPrioridad)
            #self.freeNodeList.remove(inicioConfirmacionRespuesta) #removemos el nodo que ya fue instanciado
            port, ip = self.extractPortAndIp(datos) # Extraemos la direccion del nodo que instanciaron.
            self.instantiateNode(inicioConfirmacionRespuesta, ip, port) #Instanciamos ese nodo con un puerto e ip.
             #Armamos el paquete.
            self.tcplService.sendPackage(self.assemblePackage.assemblePackageConfirmPosACK(1,numeroDeRequest), ipFuente, puertoFuente)


        elif numeroDeServicio == self.CONFIRMPOSACK: 
            self.confirmationCounters[numeroDeRequest] += 1

            #dependiendo si ya me confirmaron todos los nodos
        elif numeroDeServicio == self.CONNECT:
            #print("Si me llego un connect")
            #Cuando recibe una solicitud de conexion:
            #1- Se busca un nodo que no este instanciado
            #se pregunta a los demas nodos si lo tienen libre.
            listaPaquetes = []
            numeroDeNodo = self.requestPos(ipPort) #No hay direccion broadcast
            if numeroDeNodo is not 0: #Si no es 0 es que habia un nodo disponible.
                #print("Esta es la lista de adyacentes",numeroDeNodo , self.adyacentNodes.get(numeroDeNodo))
                listaDeAdyacencia = self.listAdyacentGenerator(numeroDeNodo)
                listaPaquetes = self.assemblePackage.assemblePackageConnectACK(package, numeroDeNodo, listaDeAdyacencia)
                for indice in range(len(listaPaquetes)): #Enviamos la lista de paquetes al nodo verde que se aba de conectar.
                    self.tcplService.sendPackage(listaPaquetes[indice], ipFuente, puertoFuente)
            #Tenemos que buscar ID
            #Hacemos request pos para los demas

    def extractPortAndIp(self, datos):
        '''
        Subrutina que extrae el puerto e ip de un bytearray
        :param datos: datos de los que se va a extraer la informacion
        :return: retorna el numero de puerto y la ip.
        '''
        ip = ""
        ip += str(datos[0]) + "."
        ip += str(datos[1]) + "."
        ip += str(datos[2]) + "."
        ip += str(datos[3])
        port = str(int.from_bytes(datos[4:5], byteorder='big'))
        return port, ip 

    def assignAddressToNode(self, id, ip, puerto): 
        pass

    def loadOrangeNeighboring(self, orangeNodes):
        listaDeIpsYpuertos = orangeNodes.split()
        #print("El tamaño de la lista es", len(listaDeIpsYpuertos))
        for i in range(0, len(listaDeIpsYpuertos), 2):
            #print(i, "\n")
            #print("Hola ",listaDeIpsYpuertos[i], "\n")
            #if self.localIp != listaDeIpsYpuertos[i]:
            self.orangeNodesList.append([listaDeIpsYpuertos[i], listaDeIpsYpuertos[i+1]])

    '''
    Genera un numero de nodo verde entre los disponibles
    Si hay nodos disponibles retorna uno generado aleatoriamente,
    De lo contrario retorna 0
    '''
    def getAvailableGreenNum(self):
        #print(len(self.freeNodeList))
        while len(self.freeNodeList):
            nodeNumIndex = random.randint(0, len(self.freeNodeList) - 1)
            #print("Numero de index ", nodeNumIndex)
            if not self.freeNodeList[nodeNumIndex] in self.instantiatingList:
                print("Generé el nombre de nodo: ", self.freeNodeList[nodeNumIndex], " aleatoriamiente")
                return self.freeNodeList[nodeNumIndex]
        return 0


    # Pregunta si un nodo ha sido instanciado a los de más nodos naranjas
    # retorna la posición instanciada
    def requestPos(self, ipPort):
        """
        Pregunta si un nodo ha sido instanciado a los de más nodos naranjas
        @:param ipPort Ip broadcast
        @:return: La posición instanciada para el nodo verde
        """
        requested = False
        while not requested:
            # Crear paquete para REQUEST_POS
            # Generar un numero aleatorio entre los disponibles
            position = self.getAvailableGreenNum()
            
            # Si se generó un 0, no hay nodos disponibles, retornamos fallo
            if position == 0:
                return 0

            # Agregar paquete a lista de nodos instanciandose
            self.instantiatingList.append(position)
            print("Instanciando nodos:", self.instantiatingList)

            #print(self.instantiatingList)
            #print(ipPort)
            # Se ensambla el paquete
            requestPosPacket = self.assemblePackage.assemblePackageRequestPos(position, self.id)
            requestNum = int.from_bytes(requestPosPacket[0:4], byteorder='big')
            self.confirmationCounters[requestNum] = 0

            # Enviamos la solicitud a todos los naranjas
            for node in self.orangeNodesList:
                ip, puerto = node
                self.tcplService.sendPackage(requestPosPacket, ip, puerto)
                # hacer broadcast

            print("Envié un request pos para: ", position, "codigo:", requestNum)
            timeout = time.time() + self.WAITFORACKTIMEOUT   # en segundo
            # esperar confirmación de todos (si tardan mas de determinado tiempo)
            while requestNum in self.confirmationCounters\
            and position in self.instantiatingList\
            and self.confirmationCounters[requestNum] < len(self.orangeNodesList)\
            and time.time() < timeout:
                ''' Acá se espera a que el hilo que recibe request aumente el contador
                respectivo para saber si todos confirmaron, pero si se eliminó la entrada,
                es porque otro naranja no aceptó el request pos '''

                # Utilizamos un pequeño delay para el ciclo
                time.sleep(self.WAITFORACKDELAY)

            ''' Si se aceptó el request pos, se puede proseguir
            notar que si no se obtuvo respuesta de todos pero tampoco una denegación,
            se instancia. '''
            if requestNum in self.confirmationCounters and position in self.instantiatingList:
                requested = True
                self.confirmationCounters.pop(requestNum) #Se saca de el diccionario y se instancia.
            else:
                print("Se me denegó request pos para: ", position)
                #return 0

        # Si se instanció la posición, lo sacamos de la lista de disponible y retornamos
        if self.confirmPos(position, ipPort):
            self.freeNodeList.remove(position)
            self.instantiatingList.remove(position)
            self.instantiateNode(position, ipPort[0], ipPort[1])
            print("Logré instanciar a nodo:", position)
            print("Lista de adyacencias:")
            self.printAdyacencyList(self.adyacentNodes)
            return position


    def listAdyacentGenerator(self,numeroNodo):
        listAdyacent = []
        for indice in self.adyacentNodes[numeroNodo]:
            #print(type(indice.id))
            #print("Añadiendo: ", self.adyacentNodes.get(indice.id)[0].id, "del nodo: ", numeroNodo)
            listAdyacent.append(self.adyacentNodes.get(indice.id)[0])
        return listAdyacent

    def requestPosACK(self, position, ipPort, packageRequest):
        """
        Envia un ACK indicando si una posición ya está instanciada o no
        @:param position posición que se determinará si esta usada o no
        @:param ipPort Ip y peurto al que se devuelve el ACK instantiated = True
        @:param packageRequest paquete request sobre el cuál se devuelve el ACK
        """
        priority = int.from_bytes(packageRequest[6:8], byteorder='big') #Estaba de 7 a 9 que si corresponden a las posiciones si se empiza a contar desde 1.
        ''' Revisamos si no está instanciado, no se está intentando instanciar y 
        el request tiene mayor prioridad. '''
        if (position in self.freeNodeList) and not (position in self.instantiatingList):
            instantiated = False #El id no esta instaciado
        else:
            instantiated = True #El id esta instaciado
        print("Recibí un request pos para: ", position, "con prioridad", priority)

        ''' Si este nodo tiene menor prioridad y se está instanciando esa misma posición, 
        debe sacar el nodo de la lista de instanciamiento. '''
        if priority < self.id and position in self.instantiatingList:
            self.instantiatingList.remove(position)
            instantiated = True

        print("Responderé al request pos con un:", instantiated)

        # Ensamblamos y enviamos el paquete según el estado de esa posición
        ackPacket = self.assemblePackage.assemblePackageRequestACK(packageRequest, instantiated)
        self.tcplService.sendPackage(ackPacket, ipPort[0], ipPort[1])

    def popPackage(self): 
        while 1:
            print("Pop package...")
            package, address = self.tcplService.receivePackage()
            hiloDeAtencionRequest = threading.Thread(target=self.attendRequests, args=(package, address))
            hiloDeAtencionRequest.start()
        pass

    # Anuncia a lo demás nodos naranajs la instanciación de un nodo verde
    # Retornta True si todos confirmaron
    def confirmPos(self, position, ipPort):
        """
    Anuncia a lo demás nodos naranjas la instanciación de un nodo verde
    @:param position posición a confirmar
    @param ipPort ip broadcast
    @:return: True si se confirmó la posición por parte de los demás naranjas
        """
        confirmed = False
        while not confirmed:
            # Crear paquete para CONFIRM_POS

            # Se ensambla el paquete
            requestPosPacket = self.assemblePackage.assemblePackageConfirmPos(position, ipPort)
            requestNum = int.from_bytes(requestPosPacket[0:4], byteorder='big')

            self.confirmationCounters[requestNum] = 0

            # Enviamos la solicitud a todos los naranjas
            for node in self.orangeNodesList:
                ip, puerto = node
                self.tcplService.sendPackage(requestPosPacket, ip, puerto)
                # hacer broadcast

            print("Envié un confirm pos para: ", position)
            timeout = time.time() + self.WAITFORACKTIMEOUT   # en segundo
            # esperar confirmación de todos (si tardan mas de determinado tiempo)
            while requestNum in self.confirmationCounters\
            and self.confirmationCounters[requestNum] < len(self.orangeNodesList)\
            and time.time() < timeout:
                ''' Acá se espera a que el hilo que recibe request aumente el contador
                respectivo para saber si todos confirmaron, pero si se eliminó la entrada,
                es porque otro naranja no aceptó el request pos '''

                # Utilizamos un pequeño delay para el ciclo
                time.sleep(self.WAITFORACKDELAY)

            # Si los demás recibieron el confirm pos, se puede proseguir
            if requestNum in self.confirmationCounters:
                confirmed = True
                self.confirmationCounters.pop(requestNum)
                print("confirm pos para: ", position, "entregado")

        return True


    def confirmPosACK(self, position, ipPort):
        """
    Envia un ACK confirmando la instanciación de una posición
    @:param position posición a confirmar
    @:param ipPort ip del nodo que hizo el request
        """
        print("Recibí un confirm pos para: ", position)
        # Ensamblamos y enviamos el ACK (ya se debio agregar la posicion de instanciado)
        ackPacket = self.assemblePackage.assemblePackageConfirmPos(position, ipPort)
        self.tcplService.sendPackage(ackPacket, ipPort[0], ipPort[1])
        
    def printAdyacencyList(self, lista):
        # La lista contiene: #nodo, ip, puerto, ¿instanciado?
        for node in lista:
            #for data in lista[node]:
            nodeinfo = lista[node][0]
            print( nodeinfo.id, nodeinfo.ip, nodeinfo.port, nodeinfo.state)
        print ("-----------")
