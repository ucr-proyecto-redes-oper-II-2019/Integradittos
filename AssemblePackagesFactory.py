import random


class AssemblePackageFactory:

    def __init__(self): 
        self.DATA_MAX_SIZE = 1009
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
        self.randomMaximo = 65000

    def assemblePackage(self, numeroDeRequest, inicioConfirmacionRespuesta, tareaARealizar, tamanoPrioridad, datos):
        """
            Subrutina que arma un paquete
            @:param numeroDeRequest numero random que identifica una request.
            @:param inicioConfirmacionRespuesta indica cual va ser la respuesta o peticion en una request.
            @:param tareaARealizar numero que identifica la tarea que se va a realizar.
            @:param datos son los datos que se quieren enviar en el paquete.
            @:return paquete ya ensamblado con los parametros entrantes.
        """
        paqueteRequestPos = bytearray(self.DATA_MAX_SIZE)
        paqueteRequestPos[self.numberRequestPos: self.numberRequestPos + self.tamNumeroRequest] = numeroDeRequest.to_bytes(
            self.tamNumeroRequest, byteorder='big')
        paqueteRequestPos[self.inicioConfirmacionRespuestaPos : self.inicioConfirmacionRespuestaPos + self.tamInicioConfirmacioRespuesta] = inicioConfirmacionRespuesta.to_bytes(
            self.tamInicioConfirmacioRespuesta, byteorder='big')
        paqueteRequestPos[self.tareaARealizarPos : self.tareaARealizarPos + self.tamTareaARealizar] = tareaARealizar.to_bytes(
            self.tamTareaARealizar, byteorder='big')
        paqueteRequestPos[self.prioridad : self.prioridad + self.tamPrioridad] = tamanoPrioridad.to_bytes(
            self.tamPrioridad, byteorder='big')
        paqueteRequestPos[self.prioridad + self.tamPrioridad : ] = datos
        return paqueteRequestPos

    def unpackPackage(self, paquete):
        """
            Subrutina que desempaquete un paquete de la siguiente forma [numero de request] [inicio/confirmacion/respuesta] [numero de servicio] [tamaño del cuepo o prioridad] [datos]
            @:param paquete que se desea desempaquetar.
            @:return: los datos que contiene el paquete.
        """
        numeroDeRequest = int.from_bytes(paquete[self.numberRequestPos:self.inicioConfirmacionRespuestaPos], byteorder='big')
        inicioConfirmacionRespuesta = int.from_bytes(paquete[self.inicioConfirmacionRespuestaPos:self.tareaARealizarPos], byteorder='big')
        numeroDeServicio = int.from_bytes(paquete[self.tareaARealizarPos:self.prioridad], byteorder='big')
        tamanoCuerpoPrioridad = int.from_bytes(paquete[self.prioridad:self.prioridad + self.tamPrioridad], byteorder='big')
        datos = paquete[self.prioridad + self.tamPrioridad:]
        return numeroDeRequest, inicioConfirmacionRespuesta, numeroDeServicio, tamanoCuerpoPrioridad, datos

    def assemblePackageRequestPos(self, numeroDeNodoAInstanciar, nodoNaranjaID):
        """
            Subrutina que ensambla un paquete de request_pos
            :return: paquete requestPos ya ensamblado.
        """
        numeroDeServicio = 205
        return self.assemblePackage(random.randrange(self.randomMaximo), numeroDeNodoAInstanciar, numeroDeServicio, nodoNaranjaID, int(0).to_bytes(1, byteorder='big'))

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
        numeroRequest, idNodoAInstanciar, tareaARealizar, prioridad, datos= self.unpackPackage(packageRequest)
        if estaInstanciado is True:
            packageRequestACK = self.assemblePackage(numeroRequest, estaOcupado, numeroDeServicio, 0, 0)
        else:
            packageRequestACK = self.assemblePackage(numeroRequest, estaLibre, numeroDeServicio, 0, 0)
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
        numeroRequest, inicioConfirmacionRespuesta, tareaARealizar, prioridad, datos = self.unpackPackage(paqueteConnect)
        # Despues de realizar to do el proceso de de reserve de nodos, para este punto debo contar con el ip y el ppuerto del verde, ademas del ID que se negocio con los demas naranjas.
        for i in listaVecinos:
            listaDePaquetesConnectACK.append(self.assemblePackage(numeroRequest, idNodoAInstanciar, numeroDeServicio, self.tamIPyPuerto, int(i).to_bytes(2, byteorder="big"))) #Aqui falta que lisrt
        return listaDePaquetesConnectACK

    def assemblePackageConfirmPos(self, nodoReservado, ipAndPort):
        numeroDeServicio = 210
        tamanoIP = 4
        tamanoPort = 2
        return self.assemblePackage(random.randrange(self.randomMaximo), nodoReservado, numeroDeServicio, tamanoIP+tamanoPort, ipAndPort)

    def assemblePackageInstanciado(self):
        pass

    def assemblePackageConfirmPosACK(self, id): 
        numeroDeServicio = 211
        return self.assemblePackage(random, id, numeroDeServicio, 0)