import tcpl

print("Test envío TCPL")
ip = input("Ingrese (IP) destino: ")
port = input("Ingrese (Puerto) destino: ")
localPort = input("Ingrese (Puerto) local: ")

tcplService = tcpl.TCPL()
tcplService.startService(localPort)

for i in range(0,20):
	packet = bytearray(1009)
	packet[0:4] = i.to_bytes(4, byteorder = 'big')
	if tcplService.sendPackage(packet, ip, port):
		print("Se logró enviar el paquete: % d" %(i))
	else:
		print("No se logró enviar el paquete: % d" %(i))
tcplService.stopService()