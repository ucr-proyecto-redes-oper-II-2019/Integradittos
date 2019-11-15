import math # floor()
import random # uniform
import socket

TCPL_MAX_MESSAGE_SIZE = 1014 # bytes. To be decided!
TCPL_TIMEOUT = 10 # ms. To be decided!
TCPL_PACKET = 0
TCPL_ACK = 1
TCPL_MAX_PACKET_NUM = 2**32
TTL_START = 10





class TCPL:
''' Clase para realizar envío y recepción de paquetes usando el protocolo TCPL. '''

	## 
	def __init__(self):
	''' Constructor de objetos de clase TCPLSender '''
		# List/ Array / Dictionary
		self._sendingBag = {}
		# List/ Array / Dictionary
		self._receivingBag = {}
		# diccionario que contiene número:resultado de un paquete al recibir su ACK
		# resultado: True si se entregó con éxito, False si no se pudo entregar (TTL = 0)
		self.resolvedPackets = {}
		# indica que se llegó al time out de la bolsa de envío
		self.timeOutReached = False
		self.packetNumber = math.floor( random.uniform(0, TCPL_MAX_PACKET_NUM) )

	## 
	def sendPackage(package, address, port):
	''' Envía el paquete package a la dirección IP v4 y número de puerto 
	específicados en address. Retorna 0 si el envío fue exitoso. '''
		# Se arma el paquete TCPL
		tcplPack = bytearray(TCPL_MAX_MESSAGE_SIZE)

		myPackNumber = self.packetNumber
		self.packetNumber = (self.packerNumber + 1) % TCPL_MAX_PACKET_NUM

		# Se agrega el encabezado
		tcplPack[0:4] = myPackNumber
		   
		tcplPack[4] = TCPL_PACKET
		tcplPack[5:] = package
		# Se mete el paquete en la bolsa
		bagItem = (tcplPack, TTL_START)	
		sendingBag[ myPackNumber ] = bagItem

		# Esperamos a que ingrese		
		while 
	
"""
		# Crear el socket para enviar
		sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sendSocket.setblocking(0)
		sendSocket.sendto(tcplPack, (address, int(port)))
"""	

		return 0

	def receivePackage():
	''' Recibe un paquete recibido, junto con la dirección IP v4 y número 
	de puerto de donde fue enviado. '''

		return 0
	

	



#  _     _ _ _
# ACK  packNumber
