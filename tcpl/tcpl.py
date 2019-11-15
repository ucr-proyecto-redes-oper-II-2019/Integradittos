TCPL_MAX_MESSAGE_SIZE = 1024 # bytes. To be decided!
TCPL_TIMEOUT = 10 # ms. To be decided!



class TCPL:
''' Clase para realizar envío y recepción de paquetes usando el protocolo TCPL. '''

	## 
	def __init__(self):
	''' Constructor de objetos de clase TCPLSender '''
		# List/ Array
		self._sendingBag = []
		# List/ Array
		self._receivingBag = []

	## 
	def sendPackage(package, address):
	''' Envía el paquete package a la dirección IP v4 y número de puerto 
	específicados en address. Retorna 0 si el envío fue exitoso. '''
		return 0

	def receivePackage():
	''' Recibe un paquete recibido, junto con la dirección IP v4 y número 
	de puerto de donde fue enviado. '''
		return 0
	

	



#  _     _ _ _
# ACK  packNumber