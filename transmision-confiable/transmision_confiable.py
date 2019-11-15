-import socket 
import threading 
import sys 
import select
import ctypes #para el memset
import time
import listaCircular

# General
DATA_MAX_SIZE = 1 + 4 + 512
#RECEIVE_TIMEOUT = 0.1
BUFFER_SIZE = 10
BUFFER_START = 0

# Para envio
SEND_TIMEOUT = 3 # en segundos
SENDING_BUFFER = listaCircular()
SENDING_BUFFER_COUNT = 0
SENDING_BUFFER_LOCK = threading.Lock()
SENDING_SN = 0
SENDING_RN = 0
FINAL_MESSAGE = generar_mensaje_final()
end_of_image = False
sending_complete = False

#UDP_IP = raw_input("Escriba el numero de ip ")
UDP_PORT = input("Escriba el numero de puerto: ")
#estoy generando un servidor con sockets. 
mi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#(Por defecto utiliza tcp y ipv4)Nos genera un nuevo socket con los valores por default
mi_socket.bind(('',int(UDP_PORT)))#Recibe dos valores que uno es el host y el otro el puerto en el que va a estar esuchando.

#mi_socket.listen(5)#Cantidad de peticiones que puede manejar un socket.(conexiones que puede tener en cola.)

def generar_mensaje_final():
	msj_final = bytearray(DATA_MAX_SIZE)
	msj_final[4] = 42
	return msj_final


#Fabian e Isaac
receiveNumber = 0 # Contador de paquetes para mantener el orden
bandera = True
ventana = listaCircular()

def recibir():
	# mi_socket.setblocking(0)#hacemos que la operacion sea nonblocking.
	#Establecemos conexion. 	
	while receiveNumber == 0:#Espera a que establezca conexion. con el paqute numero 0. 
		paqueteRecibido = mi_socket.recvfrom(516)#Recibimos el paquete. 
		if paqueteRecibido[0:3] == 0:#Leemos los primeros 4 bytes de vector 
			receiveNumber++#Aumentamos nuestro RN
			ventana.establecerInicio(receiveNumber)
			
	imagen = open("laImagen.jpg", "bw")#Abrimos un archivo donde vamos a guardar las imagenes. 
	while bandera:#Aqui vamos a recibir la imagen. 
		paqueteRecibido = mi_socket.recvfrom(516)#Recibimos paquete
		dataBytes = paqueteRecibido[1:3]#Extraemos el numero de paquete. 
		int.from_bytes(dataBytes, byorder='big')#Convertimos los bytes a int.
		if receiveNumber == dataBytes:#Si el paquete es el que estamos esperando. 
			imagen.write(paqueteRecibido[4:])#Escribimos la imagen en el archivo. 
			receiveNumber++
			ventana.establecerInicio(receiveNumber)
			while ventana.getElemento(receiveNumber) != -1):
				imagen.write(ventana.getElemento(receiveNumber)[4:])
				recieveNumber++
				ventana.establecerInicio(receiveNumber)
		else:#Sino lo guardamos en el buffer
			dataBytes = paqueteRecibido[1:3]
			int.from_bytes(dataBytes, byorder='big')
			if  receiveNumber + 10 > dataBytes:#Si se encuentra dentro de la ventana. 
				ventana.insertar(paqueteRecibido, dataBytes)
				

#Hernan y Jim		

def sending_buffering():
	in_file = open("in-small.jpg", "rb")
	SENDING_BUFFER.establecerInicio(BUFFER_START)
	while not end_of_image:
		# si SN (tomemoslo como el # mayor de secuencia en el buffer de envio) 
		# es mayor o igual al mensaje que falta de ACK (RN),
		# y hay espacio en el buffer
		if SN >= RN and SENDING_BUFFER_COUNT < BUFFER_SIZE:
			#lee 512 bytes de la imagen
			image_slice = in_file.read(512)
			# si la operacion read(512) leyó '', es el fin del archivo
			if image_slice != '':
				# 0 000 0...
				mensaje_por_enviar = bytearray(DATA_MAX_SIZE)
				# setea el encabezado
				mensaje_por_enviar[0] = 0
				mensaje_por_enviar[1:3] = SN.to_bytes(3, byteorder='big')
				# copia la porcion de la imagen en el mensaje
				mensaje_por_enviar[4:4+len(image_slice)] = image_slice 
				SENDING_BUFFER_LOCK.acquire() # region critica
				# guarda el mensaje en el buffer
				SENDING_BUFFER.insertar(mensaje_por_enviar, SN)
				# aumentamos el SN y el contador del buffer
				SN += 1
				SENDING_BUFFER_COUNT += 1
				SENDING_BUFFER_LOCK.release() # region critica
			else:
				end_of_image = True
	in_file.close()


def enviar():
	# socket non blocking
	mi_socket.setblocking(0)
	ipPort = input("IP/Port: ") #lee una linea
	ipPortLine = ipPort.split() #split a la linea
	ip = ipPortLine[0]
	port = ipPortLine[1]
	# 0 000 0...
	mensaje_por_enviar = bytearray(DATA_MAX_SIZE) 
	# empaquetar establecer conexión	
	mensaje_por_enviar[0] = 0
	mensaje_por_enviar[1:3] = bytearray({0,0,0})
	#enviar paquete
	mi_socket.sendto(mensaje_por_enviar,(ip, int(port))) 
	while not sending_complete:
		last_RN = SENDING_RN
		timeout = time.time() + SEND_TIMEOUT   # en segundos
		# mientras no se haya acabado el timeout de envio y no hayan señales de vida del receptor (ACK)
		while time.time() < timeout and last_RN == SENDING_RN:		
 			SENDING_BUFFER_LOCK.acquire() # region critica
 			for msg in range (RN, SN)
 				# podria acabarse el timeout de envio y o recibir un ACK mientras se envian los paquetes
 				#if time.time() < timeout and last_RN == SENDING_RN:
					mi_socket.sendto(lista.getElemento(msg),(ip, int(port))) 
			SENDING_BUFFER_LOCK.release() # region critica	


def recibir_ACK():
	while not sending_complete:
		ACK, addr = mi_socket.recvfrom(DATA_MAX_SIZE)
		SENDING_RN = int.from_bytes(ACK[1:3], byorder='big')

		
hilo_de_buffering = threading.Thread(target=sending_buffering) 	
hilo_de_envio = threading.Thread(target=enviar)
hilo_de_recibir_ACK = threading.Thread(target=recibir_ACK)



# "Main"
while True:
    #Esto nos genera dos valores, la conexion y la direcion 
    	#conexion, direccion = mi_socket.accept()#aqui aceptamos la peticiones.
	#mi_socket.bind((UDP_IP, UDP_PORT))
	hilo_de_envio.start()#Empezamos la ejecucion del hilo
    #mi_socket.setblocking(0)
	while True: #Lee lo que el usuario digita hasta que se presiona enter.
		respuesta, addr = mi_socket.recvfrom(1024) # para recibir lo que el servidor nos quiera enviar 
		print(respuesta)

