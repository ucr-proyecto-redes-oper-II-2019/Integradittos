from AssemblePackagesFactory import AssemblePackageFactory


class OrangeNode:
    DATA_MAX_SIZE = 1009
    listaNodosLibres = []
    id = 0
    listOrangeNodes = [[]]
    def __init__(self, id):
        self.id = id

    def loadOrangeNeighboring(self, orangeNodes):
        listaDeIpsYpuertos = orangeNodes.split()
        for i in range(0, len(listaDeIpsYpuertos), 2):
            self.listOrangeNodes.append([listaDeIpsYpuertos[i], listaDeIpsYpuertos[i+1]])

    def revisarNumeroDeNodo(self, numeroDeNodo):
        """'Si devuelve un true es que el nodo ya ha sido instanciado. """
    def instanciarNodo(self, numeroDeNodo):




