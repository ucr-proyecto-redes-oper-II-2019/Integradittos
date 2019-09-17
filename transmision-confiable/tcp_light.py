import socket 
import threading 
import sys 
import select
import ctypes #para el memset
import time

max_wait_time = 0.5
sleep_time = 0.01

#UDP_IP = raw_input("Escriba el numero de ip ")
UDP_PORT = input("Escriba el numero de puerto: ")
#estoy generando un servidor con sockets. 
mi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#(Por defecto utiliza tcp y ipv4)Nos genera un nuevo socket con los valores por default
mi_socket.bind(('',int(UDP_PORT)))#Recibe dos valores que uno es el host y el otro el puerto en el que va a estar esuchando.

#mi_socket.listen(5)#Cantidad de peticiones que puede manejar un socket.(conexiones que puede tener en cola.)


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
	mi_socket.setblocking(0) #hacemos que la operacion sea nonblocking. 
	while True:
		ipPort = input("IP/Port: ") #lee una linea
		ipPortLine = ipPort.split() #split a la linea
		ip = ipPortLine[0]
		port = ipPortLine[1]
		#print(ip, port)

		#nocion de conexión
		mensaje = bytearray(516) # 0 000 0...
		mi_socket.sendto(mensaje,(ip, int(port))) #establecer conexión

		in_file = open("in-small.jpg", "rb") #abrir imagen

		packetCounter = 0 #para control
		windowCounter = 0
		SN = 0
		RN = 0

		window = {} #ventana

		image_slice = in_file.read(512) #lee 512 bytes de la imagen

		

		while image_slice: #mientras hayan partes de la imagen por enviar
		    mensaje[4:4+len(image_slice)] = image_slice #copia la porcion de la imagen en el mensaje
		    
		    #setear encabezado
		    mensaje[0] = 0x00
		    mensaje[1:3] = SN.to_bytes(3, byteorder='big')
		    
		    mi_socket.sendto(mensaje,(ip, int(port))) #enviar paquete
		    
		    respuesta = mi_socket.recvfrom(516)
			
			waited_time = 0
			
			while waited_time < max_wait_time && :
				
				waited_time += sleep_time
				time.sleep( sleep_time_time )
				
			
			#recibir próximo paquete a enviar y recibir su numero
			#nextPacket = int(mensajeRecibido[1:4])
			#if nextPacket in window
			#	mi_socket.sendto(window[nextPacket],(ip, int(port)))
		    
		    image_slice = in_file.read(512) #tomar siguiente porciòn de la imagen
		in_file.close()


		''' asi se comenta multilinea
		input = select.select([sys.stdin],[],[],1)[0]
		if 	input: 
			value = sys.stdin.readline().rstrip()
			if(value == "1"):
				print "efe en el chat"
				sys.exit(0)
			else:
				#print "you entered %s" % value
				#le enviamos el mensaje al socket 
				lista = value.split()
				mi_socket.sendto(value,(lista[0], int(lista[1])))
		'''
hilo1 = threading.Thread(target=enviar)#Definimos la tarea de nuestro hilo.


while True:
    #Esto nos genera dos valores, la conexion y la direcion 
    	#conexion, direccion = mi_socket.accept()#aqui aceptamos la peticiones.
	#mi_socket.bind((UDP_IP, UDP_PORT))
	hilo1.start()#Empezamos la ejecucion del hilo
    #mi_socket.setblocking(0)
	while True: #Lee lo que el usuario digita hasta que se presiona enter.
		respuesta, addr = mi_socket.recvfrom(1024) # para recibir lo que el servidor nos quiera enviar 
		print(respuesta)

