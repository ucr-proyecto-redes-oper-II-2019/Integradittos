# greenNode.py
import random
import threading
from tcpl.tcpl import TCPL # en carpeta inferior
from orangeNode import GreenNodeToken
from greenMessageCodes import GreenMessageCodes
from fileSystem import FileSystem
from AssemblePackagesFactory import AssemblePackageFactory
class GreenNode:
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

        self.assemblePackage = AssemblePackageFactory()

    '''
    Etapa de inicializacion del nodo verde.
    '''
    def _initialization(self):
        # Inicializar servicios basicos
        # Solicitar unirse al grafo
        # Esperar identificacion
        # Construir tabla de enrutamiento
        self.tcpl.startService(self.myPort)
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
        tableMessage = bytearray(self.DATA_MAX_SIZE)

        # ToDo: Agregar código de enviar la tabla
        tableMessage[0:4] = random.randrange(self.MAX_RANDOM)
        tableMessage[4:6] = 0
        # tableMessage[6] = código
        tableMessage[7:9] = 0 # sin prioridad
        # ...

        for neighbour in neighboursTable:
            ip = neighboursTable[neighbour][0]
            port = neighboursTable[neighbour][1]
            self.tcpl.sendPackage(tableMessage,  port, port)

    '''
    Confirmar que la tabla de enrutamiento está actualizada (tras recibir tabla de enrutamiento)
    '''

    def _checkRouteTable(self, receivedTable, sender):
        ownTable = self.routingTable
        items = 0
        offset = 0
        while self.receivedTable[offset] != 0 and self.receivedTable[offset+2] != 0:
            items  += 1

            # 2 bytes de nodo + 2 bytes de distancia = 4 bytes
            nodeNum = int.from_bytes(self.receivedTable[offset:offset+2], byteorder='big')
            distance = int.from_bytes(self.receivedTable[offset+2:offset+4], byteorder='big')

            # Se compraran los datos con nuestra tabla
            # Si ya tenemos la ruta en la tabla checkeamos su distancia
            if nodeNum in ownTable:
                if self.receivedTable[offset+2] < ownTable[ nodeNum ][1]:
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
            package, address = self.tcpl.receivePackage()
            # Si es el nodo destino se ruteo
            destination = int.from_bytes(package[13:15], byteorder='big')
            if destination != self.graphID:
                if destination in self.routingTable:
                    ip = self.neighboursTable[ self.routingTable[destination][2] ].ip
                    port = self.neighboursTable[ self.routingTable[destination][2] ].port
                    print ("Ruteando paquete hacia ", destination, " por vecino: ", self.routingTable[destination][2], ip, port )
                    self.tcpl.sendPackage(package, ip, port)
                else:
                    print ("Mensaje hacia nodo: ", destination, " desechado, no hay entrada en la tabla de ruteo.")
            else:
                hiloDeAtencionRequest = threading.Thread(target=self.attendRequests, args=(package, address))
                hiloDeAtencionRequest.start()
        pass
     
    
    def attendRequests(self, package, ipPort):

        requestNumber, beginConfirmationAnswer, serviceNumber, sizeBodyPriority, data = self.assemblePackage.unpackPackage(package)
        if serviceNumber == self.GREET_NEIGHBOR: #Se me informa que tengo un vecino
           self.greetNeighbor(requestNumber, beginConfirmationAnswer, data)

        elif serviceNumber == self.GREET_NEIGHBOR_ACK: # recibo un ack de que mi vecino ya sabe que existo
            pass

        elif serviceNumber == self.FILE_EXISTS: #Recibo un mensaje de pregunta si un archivo existe
            self.fileExist(requestNumber, data, ipPort)
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
            self.removeFile(requestNumber)
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
        elif serviceNumber == self.SEND_ROUTE: #Se me envia la tabla de enrutamiento.
            pass
        elif serviceNumber == self.SEND_ROUTE_ACK: #Se me indica que la tabla que mande se recibio correctamente.
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
        pass


    ''' ### ### ### Solicitudes de naranjas ### ### ### '''

    '''
    Agregar un vecino nuevo y presentarse si esta instanciado.
    '''
    def _addNeighbour(self, requestPack):
        pass


    ''' ### ### ### Procedimientos dentro del mismo nodo ### ### ### '''
def greetNeighbor(self, requestNumber, beginConfirmationAnswer, data):
    port, ip = self.extractPortAndIp(data)
    self.neighboursTable[beginConfirmationAnswer] = ip, port
    package = self.assemblePackage.assemblePackageGreetNeighborACK(requestNumber)
    self.tcpl.sendPackage(package, ip, port)

def fileExist(self, requestNum, data, ipPort):
    #Hay que convertir los bytes al identificador.
    answer = self._askForFileFragments() #Este no es el metodo que hay que usar :)
    package = self.assemblePackage.assemblePackageFileExistACK(requestNum, answer)
    self.tcpl.sendPackage(package, ipPort[0], ipPort[1])

def removeFile(self, requesNum):
    #Se remueve el archivo

    #Se crea ACK
    package = self.assemblePackage.assmblePackageRemoveFileACK(requesNum)
    self.tcpl.sendPackage()
    pass

    # todo Acordar estos metodos
def extractPortAndIp(self, data):
    '''
    Subrutina que extrae el puerto e ip de un bytearray
    :param datos: datos de los que se va a extraer la informacion
    :return: retorna el numero de puerto y la ip.
    '''
    ip = ""
    ip += str(data[0]) + "."
    ip += str(data[1]) + "."
    ip += str(data[2]) + "."
    ip += str(data[3])
    port = str(int.from_bytes(data[4:6], byteorder='big'))
    return port, ip
    #def splitFile(self, fileToSplit):
    #def buildFile(self, fileName):
    #def findFile(self, fileName):
    #def findFragments(self, fileName):

