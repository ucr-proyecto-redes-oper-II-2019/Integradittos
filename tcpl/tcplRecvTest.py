import tcpl

print("Test recepción TCPL")
port = input("Ingrese (Puerto) local: ")

tcplService = tcpl.TCPL()
tcplService.startService(port)

for i in range(0,20):
	packet, address = tcplService.receivePackage()
	print("Recibí paquete:", int.from_bytes(packet[0:4], byteorder='big'), "en un paquete de", len(packet), "bytes" )
tcplService.stopService()
