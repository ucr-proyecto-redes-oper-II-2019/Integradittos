
class AssemblePackageFactory:
    numberRequestPos = 0
    inicioConfirmacionRespuestaPos = 4
    tareaARealizarPos = 6
    tamCuerpoPrioridad = 7
    tamNumeroRequest = 4
    tamInicioConfirmacioRespuesta = 2
    tamTareaARealizar = 1
    tamPrioridad = 2

    def assemblePackage(self, numeroDeRequest, inicioConfirmacionRespuesta, tareaARealizar, tamanoCuerpoPrioridad, datos = 0):
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
        paqueteRequestPos[self.tamCuerpoPrioridad : self.tamCuerpoPrioridad + self.tamPrioridad] = tamanoCuerpoPrioridad.to_bytes(
            self.tamPrioridad, byteorder='big')
        paqueteRequestPos[self.tamCuerpoPrioridad + self.tamPrioridad : ] = datos.to_bytes(
            self.tamPrioridad, byteorder='big')
        return paqueteRequestPos

    def unpackPackage(self, paquete):
        """
            Subrutina que desempaquete un paquete de la siguiente forma [numero de request] [inicio/confirmacion/respuesta] [numero de servicio] [tamaño del cuepo o prioridad] [datos]
            @:param paquete que se desea desempaquetar.
            @:return: los datos que contiene el paquete.
        """
        numeroDeRequest = int.from_bytes(paquete[self.numberRequestPos:self.inicioConfirmacionRespuestaPos], byteorder='big')
        inicioConfirmacionRespuesta = int.from_bytes(paquete[self.inicioConfirmacionRespuestaPos:self.tareaARealizarPos], byteorder='big')
        numeroDeServicio = int.from_bytes(paquete[self.tareaARealizarPos:self.tamCuerpoPrioridad], byteorder='big')
        tamanoCuerpoPrioridad = int.from_bytes(paquete[self.tamCuerpoPrioridad:self.tamCuerpoPrioridad + self.tamPrioridad], byteorder='big')
        datos = int.from_bytes(paquete[self.tamCuerpoPrioridad + self.tamPrioridad:], byteorder='big')
        return numeroDeRequest, inicioConfirmacionRespuesta, numeroDeServicio, tamanoCuerpoPrioridad, datos