import random

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
    WAITFORACKDELAY = 0.5
    WAITFORACKTIMEOUT = 5

    def __init__(self, id, port):
        self.adyacentNodes = None
        self.id = id
        self.tcplService = tcpl.TCPL()
        # Estas listas deberían ser atrributos de instancia
        self.freeNodeList = []
        self.orangeNodesList = []
        # Lista de nombres de nodos esperando por ser instanciados
        self.instantiatingList = []
        self.localPort = port


        ''' Lista (dict) utilizada para llevar registro de cuáles solicitudes
         naranja - naranja han sido confirmadas, por ejemplo, aumentar
         la entrada [546] de la solicitud REQUESTPOS con ese mismo número
        cuando se reciba un REQUESTPOSACK '''
        self.confirmationCounters = dict()


    # Inicia el nodo, creando hilos e iniciando objetos/estructuras necesarias

    # ToDo: TCPL requiere su propio hilo
    def start(self):
        self.loadOrangeNeighboring("PONERAQUIRUTABONITAENUNACONSTANTE!!!")
        self.tcplService.start(self.localPort)
        threadReceiving = threading.thread(target = self.popPackage)
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
    def loadGreenGraph(filePath):
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


    ''' INTERFACE '''

    def checkNodeNumber(self, nodeNumber):
        """Si devuelve un True es que el nodo ya ha sido instanciado. """
        self.lis
        pass

    def instantiateNode(self, numeroDeNodo):
        pass
    # Subrutina que atiende requests y actúa según la que recibe


    # Envía el nombre a un nodo verde cuándo se logró ser instanciado, además de su
    # lista de vecinos
    def sendGreenInfo(self):
        pass

    def attendRequests(self, package, ipPort):
        numeroDeRequest, inicioConfirmacionRespuesta, numeroDeServicio, tamCuerpoPrioridad, datos = AssemblePackageFactory.unpackPackage(package)

        ''' Para REQUESTPOS es mas facil si la subrutina genera el número de nodo las veces
        que sean necesarias y retorna la instanciada. Por esto no estara "position" como parámetro de la 
        funcion. '''

        if numeroDeServicio == self.REQUESTPOS:
            #Si es un request service se debe sacar un nodo verde no instanciado
            #preguntar a los demas si no lo tienen instancido
            self.requestPosACK(inicioConfirmacionRespuesta, self.orangeNodesList[tamCuerpoPrioridad], package)
        elif numeroDeServicio == self.REQUESTPOSACK:
            #Confirma que un id de nodo verde no esta usado.
            #Algun tipo de contador para cuando reciba los
            self.confirmationCounters[numeroDeRequest] = self.confirmationCounters[numeroDeRequest] + 1
        elif numeroDeServicio == self.CONFIRMPOS:
            #Debe armar un corfirm pos ack
            self.freeNodeList.remove(inicioConfirmacionRespuesta) #removemos el nodo que ya fue instanciado
            ip = ""
            ip += str(int(datos[0]).to_bytes(1, byteorder='big')) + "."
            ip += str(int(datos[1]).to_bytes(1, byteorder='big')) + "."
            ip += str(int(datos[2]).to_bytes(1, byteorder='big')) + "."
            ip += str(int(datos[3]).to_bytes(1, byteorder='big'))
            port = str(int(datos[4:]).to_bytes(2, byteorder='big'))
            self.adyacentNodes.get(inicioConfirmacionRespuesta)[0].ip = ip
            self.adyacentNodes.get(inicioConfirmacionRespuesta)[0].port = port
            self.adyacentNodes.get(inicioConfirmacionRespuesta)[0].state = True
            AssemblePackageFactory.assemblePackageConfirmPosACK(1)
            pass
        elif numeroDeServicio == self.CONFIRMPOSACK:
            pass
            #dependiendo si ya me confirmaron todos los nodos
        elif numeroDeServicio == self.CONNECT:
            pass
            #Tenemos que buscar ID
            #Hacemos request pos para los demas




    def loadOrangeNeighboring(self, orangeNodes):
        listaDeIpsYpuertos = orangeNodes.split()
        for i in range(0, len(listaDeIpsYpuertos), 2):
            self.listOrangeNodes.append([listaDeIpsYpuertos[i], listaDeIpsYpuertos[i+1]])

    '''
    Genera un numero de nodo verde entre los disponibles
    Si hay nodos disponibles retorna uno generado aleatoriamente,
    De lo contrario retorna 0
    '''
    def getAvailableGreenNum(self):
        while len(self.freeNodeList):
            nodeNumIndex = random.randint(1, len(self.freeNodeList))
            if not self.freeNodeList[nodeNumIndex] in self.instantiatingList:
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
            position = self.getAvailableGreen()

            # Si se generó un 0, no hay nodos disponibles, retornamos fallo
            if position == 0:
                return 0

            # Agregar paquete a lista de nodos instanciandose
            self.instantiatingList.append(position)

            # Se ensambla el paquete
            requestPosPacket = AssemblePackageFactory.assemblePackageRequest(position, self.id)
            requestNum = int.from_bytes(receivedPacket[0:4], byteorder='big')
            self.confirmationCounters[requestNum] = 0

            # Enviamos la solicitud a todos los naranjas
            for node in self.orangeNodesList:
                # hacer broadcast

            timeout = time.time() + WAITFORACKTIMEOUT   # en segundo
            # esperar confirmación de todos (si tardan mas de determinado tiempo)
            while requestNum in confirmationCounters\
            and position in self.instantiatingList\
            and self.confirmationCounters[requestNum] < len(orangeNodesList)\
            and time.time() < timeout:
                ''' Acá se espera a que el hilo que recibe request aumente el contador
                respectivo para saber si todos confirmaron, pero si se eliminó la entrada,
                es porque otro naranja no aceptó el request pos '''

                # Utilizamos un pequeño delay para el ciclo
                sleep(self.WAITFORACKDELAY)

            ''' Si se aceptó el request pos, se puede proseguir
            notar que si no se obtuvo respuesta de todos pero tampoco una denegación,
            se instancia. '''
            if requestNum in confirmationCounters and position in self.instantiatingList:
                requested = True
                confirmationCounters.pop(requestNum)
            else:
                return 0

        # Si se instanció la posición, lo sacamos de la lista de disponible y retornamos
        if confirmPos(position, ipPort):
            self.freeNodeList.pop(position)
            self.instantiatingList.pop(position)
            return position




    def requestPosACK(self, position, ipPort, packageRequest):
        """
        Envia un ACK indicando si una posición ya está instanciada o no
        @:param position posición que se determinará si esta usada o no
        @:param ipPort Ip y peurto al que se devuelve el ACK instantiated = True
        @:param packageRequest paquete request sobre el cuál se devuelve el ACK
        """
        priority = int.from_bytes(packageRequest[7:9], byteorder='big')
        ''' Revisamos si no está instanciado, no se está intentando instanciar y 
        el request tiene mayor prioridad. '''
        if (position in freeNodeList) and not (position in instantiatingList) and (priority > self.id):
            instantiated = False
        else:
            instantiated = True

        ''' Si este nodo tiene menor prioridad y se está instanciando esa misma posición, 
        debe sacar el nodo de la lista de instanciamiento. '''
        if priority > self.id and position in self.instantiatingList:
            self.instantiatingList.pop(position)
        # Ensamblamos y enviamos el paquete según el estado de esa posición
        ackPacket = assemblePackageRequestPosACK(packageRequest, instantiated)
        tcplService.sendPackage(ackPacket, ipPort[0], ipPort[1])



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
            requestPosPacket = assemblePackageRequestPos(position, ipPort)
            requestNum = int.from_bytes(receivedPacket[0:4], byteorder='big')

            self.confirmationCounters[requestNum] = 0

            # Enviamos la solicitud a todos los naranjas
            for node in self.orangeNodesList:
                # hacer broadcast

            timeout = time.time() + WAITFORACKTIMEOUT   # en segundo
            # esperar confirmación de todos (si tardan mas de determinado tiempo)
            while requestNum in confirmationCounters\
            and self.confirmationCounters[requestNum] < len(orangeNodesList)\
            and time.time() < timeout:
                ''' Acá se espera a que el hilo que recibe request aumente el contador
                respectivo para saber si todos confirmaron, pero si se eliminó la entrada,
                es porque otro naranja no aceptó el request pos '''

                # Utilizamos un pequeño delay para el ciclo
                sleep(self.WAITFORACKDELAY)

            # Si se aceptó el request pos, se puede proseguir
            if requestNum in confirmationCounters:
                confirmed = True
                confirmationCounters.pop(requestNum)
        return True


    def confirmPosACK(self, position, ipPort):
        """
    Envia un ACK confirmando la instanciación de una posición
    @:param position posición a confirmar
    @:param ipPort ip del nodo que hizo el request
        """
        # Ensamblamos y enviamos el ACK (ya se debio agregar la posicion de instanciado)
        ackPacket = assemblePackageConfirmPos(position, ipPort)
        tcplService.sendPackage(ackPacket, ipPort[0], ipPort[1])

