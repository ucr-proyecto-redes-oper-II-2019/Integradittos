import random


class AssemblePackageFactory:

    def __init__(self):
        self.DATA_MAX_SIZE = 1015
        #Posiciones
        self.numberRequestPos = 0
        self.inicioConfirmacionRespuestaPos = 4
        self.tareaARealizarPos = 6
        self.prioridad = 7
        #Tamaños
        self.tamNumeroRequest = 4
        self.tamInicioConfirmacioRespuesta = 2
        self.tamTareaARealizar = 1
        self.tamPrioridad = 2
        self.tamIPyPuerto = 8
        self.tamTTL = 2
        self.tamFuente = 2
        self.TamDestino = 2
        self.randomMaximo = 65000

    def assemblePackage(self, numeroDeRequest, inicioConfirmacionRespuesta, tareaARealizar, tamanoPrioridad, TTL, fuente, destino, datos):
        """
            Subrutina que arma un paquete
            @:param numeroDeRequest numero random que identifica una request.
            @:param inicioConfirmacionRespuesta indica cual va ser la respuesta o peticion en una request.
            @:param tareaARealizar numero que identifica la tarea que se va a realizar.
            @:param datos son los datos que se quieren enviar en el paquete.
            @:return paquete ya ensamblado con los parametros entrantes.
        """
        paquete = bytearray(self.DATA_MAX_SIZE)
        paquete[0:4] = numeroDeRequest.to_bytes(self.tamNumeroRequest, byteorder='big')
        paquete[4:6] = inicioConfirmacionRespuesta.to_bytes(self.tamInicioConfirmacioRespuesta, byteorder='big')
        paquete[6] = tareaARealizar
        paquete[7:9] = tamanoPrioridad.to_bytes(self.tamPrioridad, byteorder='big')
        paquete[9:11] = TTL.to_bytes(self.tamTTL, byteorder='big')
        paquete[11:13] = fuente.to_bytes(self.tamFuente, byteorder='big')
        paquete[13:15] = destino.to_bytes(self.TamDestino, byteorder='big')
        paquete[15:] = datos
        return paquete

    def unpackPackage(self, paquete):
        """
            Subrutina que desempaquete un paquete de la siguiente forma [numero de request] [inicio/confirmacion/respuesta] [numero de servicio] [tamaño del cuepo o prioridad] [datos]
            @:param paquete que se desea desempaquetar.
            @:return: los datos que contiene el paquete.
        """
        numeroDeRequest = int.from_bytes(paquete[0:4], byteorder='big')
        inicioConfirmacionRespuesta = int.from_bytes(paquete[4:6], byteorder='big')
        numeroDeServicio = paquete[6]
        tamanoCuerpoPrioridad = int.from_bytes(paquete[7:9], byteorder='big')
        ttl = int.from_bytes(paquete[9:11], byteorder='big')
        fuente = int.from_bytes(paquete[11:13], byteorder='big')
        destino = int.from_bytes(paquete[13:15], byteorder='big')
        datos = paquete[15:]
        return numeroDeRequest, inicioConfirmacionRespuesta, numeroDeServicio, tamanoCuerpoPrioridad, ttl, fuente, destino, datos

    def assemblePackageRequestPos(self, numeroDeNodoAInstanciar, nodoNaranjaID):
        """
            Subrutina que ensambla un paquete de request_pos
            :return: paquete requestPos ya ensamblado.
        """
        numeroDeServicio = 205
        numeroRand = random.randrange(self.randomMaximo)
        #print("El numero de reques que se esta generando es: ", numeroRand )
        return self.assemblePackage(numeroRand, numeroDeNodoAInstanciar, numeroDeServicio, nodoNaranjaID, 50, 0, 0, int(0).to_bytes(1, byteorder='big'))

    def assemblePackageRequestACK(self, packageRequest, estaInstanciado):
        """
            Subrutina que emsambla un ACK para un paquete request ACK.
            @:param packageRequest: paquete request para el que se desea generar respuesta.
            @:param estaInstanciado boolean que avisa si un nodo ya esta instanciado para poder generar ACK correctamente.
            :return: paquete respuesta.
        """
        packageRequestACK = bytearray(self.DATA_MAX_SIZE)
        numeroDeServicio = 206
        estaOcupado = 0
        estaLibre = 1
        numeroRequest, idNodoAInstanciar, tareaARealizar, prioridad,ttl, fuente, destino,  datos= self.unpackPackage(packageRequest)
        if estaInstanciado == 0:
            packageRequestACK = self.assemblePackage(numeroRequest, estaOcupado, numeroDeServicio, 0, 50 ,0 ,0,int(0).to_bytes(1, byteorder='big'))
        else:
            packageRequestACK = self.assemblePackage(numeroRequest, estaLibre, numeroDeServicio, 0, 50, 0, 0, int(0).to_bytes(1, byteorder='big'))
        return packageRequestACK

    def assemblePackageConnectACK(self, paqueteConnect, idNodoAInstanciar, listaVecinos):
        """
            Subrutina que arma un ack par un paquete de tipo connect
            :param paqueteConnect:  paquete connect recibido
            :param idNodoAInstanciar: id del nodo que se aprobo su instanaciacion.
            :param listaVecinos: lista de vecinos del id del nodo que se va a instancias.
            :return: lista de paquetes que se le debe enviar al que solicito el request.
        """
        numeroDeServicio = 201
        listaDePaquetesConnectACK = []
        numeroRequest, inicioConfirmacionRespuesta, tareaARealizar, prioridad, ttl, fuente, destino,  datos = self.unpackPackage(paqueteConnect)
        # Despues de realizar to do el proceso de de reserve de nodos, para este punto debo contar con el ip y el ppuerto del verde, ademas del ID que se negocio con los demas naranjas.
        paquete = bytearray(8)
        for vecino in listaVecinos:
            paquete[0:2] = int(vecino.id).to_bytes(2, byteorder="big") #Id del nodo
            arrayIPandPort = self.packIpPort(vecino.ip, vecino.port)
            paquete[2:6] = arrayIPandPort[0:4]
            paquete[6:8] = arrayIPandPort[4:]
            listaDePaquetesConnectACK.append(self.assemblePackage(numeroRequest, idNodoAInstanciar, numeroDeServicio, self.tamIPyPuerto, 50, 0, 0, paquete)) #Aqui falta que lisrt
        return listaDePaquetesConnectACK

    def assemblePackageConfirmPos(self, nodoReservado, ipAndPort):
        numeroDeServicio = 210
        tamanoIP = 4
        tamanoPort = 2
        return self.assemblePackage(random.randint(0,self.randomMaximo), nodoReservado, numeroDeServicio, tamanoIP+tamanoPort, 50, 0, 0, self.packIpPort(ipAndPort[0],ipAndPort[1]))

    def assemblePackageInstanciado(self):
        pass

    def assemblePackageConfirmPosACK(self, id, requestNum):
        numeroDeServicio = 211
        return self.assemblePackage(requestNum, id, numeroDeServicio, 0 , 50, 0, 0, int(0).to_bytes(1, byteorder='big'))

    def assemblePackageGreetNeighbor(self, id, fuente, destino):
        numeroDeServicio = 100
        return self.assemblePackage(random.randint(0,self.randomMaximo), id, numeroDeServicio, 0 , 50, fuente, destino, int(0).to_bytes(1, byteorder='big'))

    def assemblePackageGreetNeighborACK(self, requestNum, fuente, destino):
        numeroDeServicio = 101
        return self.assemblePackage(requestNum, 0, numeroDeServicio, 0 , 50, fuente, destino, int(0).to_bytes(1, byteorder='big'))

    def assemblePackageFileExistACK(self, requestNum, answer):
        numeroDeServicio = 103
        return self.assemblePackage(requestNum, 0, numeroDeServicio, 0, 50, 0, 0, int(answer).to_bytes(1, byteorder='big'))

    def assmblePackageRemoveFileACK(self, requesNum):
        numeroDeServicio = 109
        return self.assemblePackage(requesNum, 0, numeroDeServicio, 1, 50, 0, 0, int(0).to_bytes(1, byteorder='big'))

    def assemblePackageConnect(self):
        numeroDeServicio = 200
        return self.assemblePackage(random.randint(0,self.randomMaximo), 1, numeroDeServicio, 0, 50, 0, 0, int(0).to_bytes(1, byteorder='big'))


    def packIP(self, ip):
        arrayIP = bytearray(4)
        ipSplit = str(ip).split(".")
        arrayIP[0] = int(ipSplit[0])
        arrayIP[1] = int(ipSplit[1])
        arrayIP[2] = int(ipSplit[2])
        arrayIP[3] = int(ipSplit[3])
        return arrayIP

    def packPort(self, port):
        return int(port).to_bytes(2, byteorder='big')

    def packIpPort(self, ip, port):
        arrayIP = bytearray(6)
        ipSplit = str(ip).split(".")
        if len(ipSplit) == 4:
            #print("arreglo ip split ", ipSplit)
            arrayIP[0] = int(ipSplit[0])
            arrayIP[1] = int(ipSplit[1])
            arrayIP[2] = int(ipSplit[2])
            arrayIP[3] = int(ipSplit[3])
            arrayIP[4:] = int(port).to_bytes(2, byteorder='big')
        return arrayIP
