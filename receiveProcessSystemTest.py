from processSystem import ProcessSystem
import sys


nombre = sys.argv[1]
ejecutable = sys.argv[2]
puerto = sys.argv[3]

psys = ProcessSystem(puerto, True)

psys.receiveProcess(nombre, ejecutable, puerto)

psys.executeProcess(nombre)
