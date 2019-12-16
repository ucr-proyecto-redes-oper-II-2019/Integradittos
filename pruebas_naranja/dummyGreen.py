from AssemblePackagesFactory import AssemblePackageFactory
from tcpl.tcpl import TCPL
import threading


def recibirInfo():
    packet, address = tcplService.receivePackage()
    numeroDeRequest, inicioConfirmacionRespuesta, numeroDeServicio, tamCuerpoPrioridad, datos = factoria.unpackPackage(
        packet)
    print("ID = ", inicioConfirmacionRespuesta)
    while 1:
        packet, address = tcplService.receivePackage()
        numeroDeRequest, inicioConfirmacionRespuesta, numeroDeServicio, tamCuerpoPrioridad, datos = factoria.unpackPackage(
            packet)
        print("Vecino = ", int.from_bytes(datos[0:2], byteorder='big'))
        ipValue = int.from_bytes(datos[2:6], byteorder='big')
        if ipValue != 0:
            print("IP:", datos[2], ".", datos[3], ".", datos[4], ".", datos[5], "Puerto:", int.from_bytes(datos[6:8], byteorder='big'))
        else:
            print("No esta instanciado")
puerto = input("Ingrese su puerto: ")
ipNaranja = input("Ingrese IP naranja: ")
puertoNaranja = input("Ingrese puerto naranja: ")
tcplService = TCPL()
tcplService.startService(puerto)
factoria = AssemblePackageFactory()
paquete = factoria.assemblePackage(37, 1, 200, 1, int(1).to_bytes(256, byteorder='big'))
enviado = tcplService.sendPackage(paquete, ipNaranja, puertoNaranja)
print(enviado)
if (enviado):
    print("Esperando respuesta naranja")
    threadReceiving = threading.Thread(target=recibirInfo())
    threadReceiving.start()
    threadReceiving.join()

else:
    print("Fallo")

tcplService.stopService()