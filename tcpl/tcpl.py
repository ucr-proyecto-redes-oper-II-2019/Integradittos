import math # floor()
import random # uniform
import socket
import threading
import time

TCPL_MAX_MESSAGE_SIZE = 1014 # bytes. A decidir!
TCPL_TIMEOUT = 1 # segs. A decidir!
TCPL_PACKET = 0 # 0 para solicitud
TCPL_ACK = 1 # 1 para ACK
TCPL_MAX_PACKET_NUM = 2**32 # 4 bytes para num. de solicitud
TTL_START = 10 # "TTL" de los paquetes en la bolsa
ASK_FOR_RESOLVE = 1  # segs. Retardo para checkear lista de paquetes resueltos


class TCPL:
	''' Clase para realizar envío y recepción de paquetes usando el protocolo TCPL. '''

	## 
	def __init__(self):
		''' Constructor de objetos de clase TCPLSender. '''
		# List/ Array / Dictionary
		self.sendingBag = {}
		self.sendingBagLock = threading.Lock() 
		# List/ Array / Dictionary
		self.receivingBag = {}
		self.sendingBagLock = threading.Lock() 
		# diccionario que contiene número:resultado de un paquete al recibir su ACK
		# resultado: True si se entregó con éxito, False si no se pudo entregar (TTL = 0)
		self.resolvedPackets = {}
		# indica que se llegó al time out de la bolsa de envío
		self.timeOutReached = False
		# Número de paquete inicial (aleatorio)
		self.packetNumber = math.floor( random.uniform(0, TCPL_MAX_PACKET_NUM) )
		# Bandera para indicar si el objeto TCPL se encuentra enviando/recibiendo
		self.serviceUp = True
		# Socket del servicio
		self.tcplSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		


	##
	def startService(self, port):
		''' Inicia el servicio TCPL, osea, la ejecución de los hilos de envío y 
		recepción que trabajan sobre las "bolsas" respectivas 
		
		port: puerto de escucha de paquetes TCPL
		'''
		self.tcplSocket.bind(('', int(port)))
		self.tcplSocket.setblocking(0)
		# Se inician los hilos den envío y recepción
		sendThread = threading.Thread(target = self.bagSending)
		recvThread = threading.Thread(target = self.bagReceiving, args = (port,))
		sendThread.start()
		recvThread.start()
	
	##
	def stopService(self):
		''' Esta subrutina detiene manda a terminar los hilos de envío y recepción '''
		self.serviceUp = False

	## 
	def sendPackage(self, package, address, port):
		''' Envía el paquete package a la dirección IP v4 y número de puerto 
		específicados en address. Retorna 0 si el envío fue exitoso. 

		package: el paquete de capa superior a enviar usando TCPL
		address: dirección destino
		port: puerto destino
		return True si el paquete fue entregado, False si no
		'''
		# Valor de retorno
		delivered = False

		# Se arma el paquete TCPL
		tcplPack = bytearray(TCPL_MAX_MESSAGE_SIZE)
		myPackNumber = self.packetNumber
		# Aumentamos el número para el siguiente número de paquete
		self.packetNumber = (self.packetNumber + 1) % TCPL_MAX_PACKET_NUM
		# Se agrega el encabezado
		tcplPack[0:4] = myPackNumber.to_bytes(4, byteorder = 'big')
		tcplPack[4] = TCPL_PACKET
		tcplPack[5:] = package

		# Se mete el paquete en la bolsa (con su IP:Puerto y TTL para el hilo de envío)
		bagItem = [tcplPack, address, port, TTL_START]
		self.sendingBag[ myPackNumber ] = bagItem

		# Esperamos a que ingrese		
		while not (myPackNumber in self.resolvedPackets):
			time.sleep(ASK_FOR_RESOLVE)
		# Se resolvió el paquete, se revisa si se entregó o no se pudo enviar
		# Si se resolvió con la entrega, el valor de retorno será True
		# sino, se mantiene el False (el TTL del paquete en la bolsa expiró)
		if self.resolvedPackets[myPackNumber] == True:
			delivered = True
		self.resolvedPackets.pop(myPackNumber)

		return delivered

	##
	def bagSending(self):
		''' Función destinada al hilo encargado de enviar los paquetes
		que ingresan a la bolsa de envío. 
		'''
		# Entramos en el ciclo para enviar
		while self.serviceUp:
			# Si hay paquetes en la bolsa, podemos enviarlos
			if self.sendingBag:
				self.sendingBagLock.acquire()
				# OJO: un for por sobre un diccionario itera por las llaves, no por sos valores
				for bagItem in list(self.sendingBag.keys()):
					# Item en bolsa:
					# sendingBag[bagItem][0] = paquete
					# sendingBag[bagItem][1] = ip
					# sendingBag[bagItem][2] = puerto
					# sendingBag[bagItem][3] = TTL
					self.tcplSocket.sendto(self.sendingBag[bagItem][0], (self.sendingBag[bagItem][1], int(self.sendingBag[bagItem][2])) )
					# Restamos 1 al TTL
					self.sendingBag[bagItem][3] -= 1
					# Si el TTL es igual a 0, sacamos el paquete de la cola y lo 
					# resolvemos como no entregado
					if self.sendingBag[bagItem][3] == 0:
						# packet[0] contiene el paquete con header incluido (0:5)
						packetNum =  int.from_bytes(self.sendingBag[bagItem][0][0:4], byteorder='big')
						self.sendingBag.pop( packetNum )
						self.resolvedPackets[packetNum] = False
				self.sendingBagLock.release()
			# Esperamos por el timeout para reenviar los paquetes en la bolsa 
			time.sleep(TCPL_TIMEOUT)

	##
	def receivePackage(self):
		''' Saca un paquete de la bolsa de recibidos. '''
		# Esperamos a que hayan paquetes en la bolsa
		while not len(self.receivingBag):
			time.sleep(TCPL_TIMEOUT)
		# Sacamos un paquete para retornarlo.
		receivedPacket, address = self.receivingBag.get(list(self.receivingBag.keys())[0])
		print("PERRO ME LLEGO EL PAQUETE.")
		self.receivingBag.pop(list(self.receivingBag.keys())[0])
		# Los primeros 5 bytes son de header TCPL
		return receivedPacket[5:], address

	##
	def bagReceiving(self, port):
		''' Función destinada al hilo encargado de recibir los paquetes
		que ingresan al servicio y: meterlos a la bolsa de recibidos y enviar
		un ACK, o: Resolver un paquete enviado si se recibió un ACK. 

		port: puerto local para paquetes recibidos
		'''

		while self.serviceUp:
			# senderAdress es una tupla ip:puerto
			try:
				receivedPacket, senderAddress = self.tcplSocket.recvfrom(TCPL_MAX_MESSAGE_SIZE)
			except socket.error:
				receivedPacket = None
			if receivedPacket is not None:
				packetNum = int.from_bytes(receivedPacket[0:4], byteorder='big')
				# Revisamos si es una solicitud (0) o un ACK (1)
				if receivedPacket[4] == 0:
					# Se agrega el paquete recbido a la bolsa de recibidos (si no es repetido)
					if not (packetNum in self.receivingBag):
						self.receivingBag[packetNum] = receivedPacket, senderAddress
					# Armamos el ACK y se envía
					tcplACK = bytearray(TCPL_MAX_MESSAGE_SIZE)
					tcplACK[0:4] = packetNum.to_bytes(4, byteorder = 'big')
					tcplACK[4] = TCPL_ACK
					self.tcplSocket.sendto(tcplACK, senderAddress)
				elif receivedPacket[4] == 1:
					self.sendingBagLock.acquire()
					if packetNum in self.sendingBag:
						# Sacamos el paquete de la bolsa de envío y agregamos
						# su número a la lista de resueltos (True = entregado)
						self.sendingBag.pop(packetNum)
						self.resolvedPackets[packetNum] = True
					self.sendingBagLock.release()

