import socket 
import threading 
import sys 
import select
import ctypes #para el memset
import time

DATA_MAX_SIZE = 1 + 4 + 512
RECEIVE_TIMEOUT = 0.1
FINAL_MESSAGE = generar_mensaje_final()

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
#ventana = dict()
inicioArrCir = 0

def recibir():
	# mi_socket.setblocking(0)#hacemos que la operacion sea nonblocking.
	
	while receiveNumber == 0:#Espera a que establezca conexion. con el paqute numero 0. 
		paqueteRecibido = mi_socket.recvfrom(516)#Recibimos el paquete. 
		if paqueteRecibido[0:3] == 0:#Leemos los primeros 4 bytes de vector 
			receiveNumber++#Aumentamos nuestro RN
	imagen = open("laImagen.jpg", "bw")#Abrimos un archivo donde vamos a guardar los
	while bandera:#Aqui esperamos hasta recibir el ultimo. 
		paqueteRecibido = mi_socket.recvfrom(516)#Recibimos paquete
		bytes = paqueteRecibido[1:3]
		int.from_bytes(bytes, byorder='big')#Convertimos los bytes a int.
		if receiveNumber == bytes:#Leemos para saber que numero de paquete es 
			imagen.write(paqueteRecibido[4:])
			receiveNumber++
			while recieveNumber == ventana.has_key(recieveNumber):
				imagen.write(ventana.get(recieveNumber, default=0))
				#ventana.pop(recieveNumber,None)
				recieveNumber++
		else:
			if len(ventana) < 10:
				bytes = paqueteRecibido[1:3]
				int.from_bytes(bytes, byorder='big')
				#ventana.

#Hernan y Jim
def enviar():
	# se aplica un timeout para el socket.
	mi_socket.settimeout(RECEIVE_TIMEOUT)

	while True:
		ipPort = input("IP/Port: ") #lee una linea
		ipPortLine = ipPort.split() #split a la linea
		ip = ipPortLine[0]
		port = ipPortLine[1]
		#print(ip, port)

		#nocion de conexión
		mensaje_por_enviar = bytearray(DATA_MAX_SIZE) # 0 000 0...
		mi_socket.sendto(mensaje_por_enviar,(ip, int(port))) #establecer conexión

		in_file = open("in-small.jpg", "rb") #abrir imagen

		# indice del paquete que se está enviando
		packet_counter = 0 
		
		SN = 0
		RN = 0

		image_slice = in_file.read(512) #lee 512 bytes de la imagen

		trabajo_pendiente = true

		while image_slice: #mientras hayan partes de la imagen por enviar

		    mensaje_por_enviar[4:4+len(image_slice)] = image_slice #copia la porcion de la imagen en el mensaje
		    
		    #setear encabezado
		    mensaje_por_enviar[0] = 0x00
		    mensaje_por_enviar[1:3] = SN.to_bytes(3, byteorder='big')
		    
		    mi_socket.sendto(mensaje_por_enviar,(ip, int(port))) #enviar paquete
		    
		    try:
				respuesta, addr = mi_socket.recvfrom(DATA_MAX_SIZE)
				answer_number = int.from_bytes(bytearray(respuesta[1:3]), byteorder='little') ############## Little endian

				# if the receiver is asking for the next package:
				if (answer_number == packet_counter + 1)
					packet_counter += 1
					image_slice = in_file.read(512)

			except socket.timeout:
				# no se recibio ningun paquete
				# por esto, se vuelve a intentar enviar el paquete actual
		in_file.close()
		
hilo_de_envio = threading.Thread(target=enviar)#Definimos la tarea de nuestro hilo.


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

