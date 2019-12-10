import tcpl

print("Test recepción TCPL")
port = input("Ingrese (Puerto) local: ")

tcplService = tcpl.TCPL()
tcplService.startService(port)
'''
for i in range(0,20):
	packet, address = tcplService.receivePackage()
	print("Recibí paquete:", int.from_bytes(packet[0:4], byteorder='big'), "en un paquete de", len(packet), "bytes" )
'''
packet, address = tcplService.receivePackage()
items = 0
offset = 0
while packet[offset] != 0 and packet[offset+1] != 0:
	items  += 1
	offset += 2
print("Recibi una tabla de tamaño: ", items)
print("El primer elemento es: ", packet[0], packet[1])
tcplService.stopService()
