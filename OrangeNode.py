from AssemblePackagesFactory import AssemblePackageFactory


class OrangeNode:
    DATA_MAX_SIZE = 1009
    listaNodosLibres = []
    id = 0
    listOrangeNodes = []
    def __init__(self, id):
        self.id = id
    def assemblePackageRequestPos(self):
        """
            Subrutina que ensambla un paquete de request_pos
            :return: paquete requestPos ya ensamblado.
        """
        numeroDeServicio = 205
        nodoLibre = self.getNodoNoInstanciado()
        return AssemblePackageFactory.assemblePackage(numeroDeServicio, nodoLibre, self.id)

    def assemblePackageRequestACK(self, paquete):
        """
            Subrutina que emsambla un ACK para un paquete request ACK.
            :param paquete: paquete request para el que se desea generar respuesta.
            :return: paquete respuesta.
        """
        numeroDeServicio = 206
        estaOcupado = 0
        estaLibre = 1
        numeroRequest, idNodoAInstanciar, tareaARealizar, prioridad = self.unpackPackage(paquete)
        if self.revisarNumeroDeNodo(idNodoAInstanciar):
            AssemblePackageFactory.assemblePackage(numeroRequest, estaOcupado, numeroDeServicio, 0)
        else:
            AssemblePackageFactory.assemblePackage(numeroRequest, estaLibre, numeroDeServicio, 0)

    def assemblePackageConnectACK(self):

    def assemblePackageConfirmPos(self):

    def assemblePackageInstanciado(self):

    def revisarNumeroDeNodo(self, numeroDeNodo):
        """'Si devuelve un true es que el nodo ya ha sido instanciado. """
    def instanciarNodo(self, numeroDeNodo):




