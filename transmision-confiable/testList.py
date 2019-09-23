from listaCircular import listaCircular
import numpy

lista = listaCircular()
lista.establecerInicio(0)
for x in range (0,12):
	print("Insertando: %d" % (x))
	paquete = bytearray(4)
	paquete[1:3] = x.to_bytes(3, byteorder='big')
	lista.insertar(paquete, x)
for x in range (0,9):
	numBytes = bytearray(4)
	numBytes = lista.getElemento(x)
	num = int.from_bytes(numBytes, byteorder='big')
	print("Posicion %d: %d" % (x, num))
	
