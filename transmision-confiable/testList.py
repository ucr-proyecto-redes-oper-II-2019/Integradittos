from listaCircular import listaCircular


lista = listaCircular()
#lista.init(10)
lista.establecer_inicio(0)
for x in range (0,12):
	print("Insertando: %d" % (x) )
	paquete = bytearray(4)# [][][][] un paquete de 4 bytes.
	paquete[1:3] = x.to_bytes(3, byteorder='big')

	lista.insertar(paquete, x)
	#print(paquete)
for x in range (0,9):
	numBytes = bytearray(4)
	numBytes = lista.get_elemento(x)
	print(numBytes)
	if numBytes != -1:
		num = int.from_bytes(numBytes[1:4], byteorder='big')
		print("Posicion %d: %d" % (x, num))
	else:
		print("no esta", numBytes)
	
