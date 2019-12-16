from processSystem import ProcessSystem
import sys


puerto = sys.argv[1]
ipDestino = sys.argv[2]
puertoDestino = sys.argv[3]
nombre = sys.argv[4]
filesList = sys.argv[5:]


psys = ProcessSystem(puerto, False)

psys.sendProcess(nombre, filesList, ipDestino, puertoDestino, puerto)
