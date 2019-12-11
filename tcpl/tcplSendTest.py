import tcpl

print("Test envío TCPL")
ip = input("Ingrese (IP) destino: ")
port = input("Ingrese (Puerto) destino: ")
localPort = input("Ingrese (Puerto) local: ")

tcplService = tcpl.TCPL()
tcplService.startService(localPort)
'''
for i in range(0,20):
	packet = bytearray(25)
	packet[0:4] = i.to_bytes(4, byteorder = 'big')
	if tcplService.sendPackage(packet, ip, port):
		print("Se logró enviar el paquete:", i)
	else:
		print("No se logró enviar el paquete:", i)
'''

rountingTable = dict()
rountingTable[1] = (2,1,1)
rountingTable[3] = (6,2,1)
rountingTable[5] = (7,2,1)

table = bytearray(1000)
offset = 0
for node in rountingTable:
			table[offset] = rountingTable[node][0] # nodo
			table[offset+1] = rountingTable[node][1] # distancia
			offset += 2
if tcplService.sendPackage(table, ip, port):
	print("Se logró enviar el paquete")
else:
	print("No se logró enviar el paquete")

tcplService.stopService()
