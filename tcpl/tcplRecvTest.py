import tcpl

print("Test recepción TCPL")
port = input("Ingrese (Puerto) local: ")

tcplService = tcpl.TCPL()
tcplService.startService(port)

for i in range(0,20):
	packet, address = tcplService.receivePackage()
	print("Recibí paquete: % d" %(int.from_bytes(packet[0:4], byteorder='big')) )
tcplService.stopService()
