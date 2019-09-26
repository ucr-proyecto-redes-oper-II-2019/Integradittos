import socket 
import threading 
import sys 
import select
import ctypes #para el memset
import time
import listaCircular
from time import time

#Fabian e Isaac. 

class Receptor:
	sn = 0#Send number  
	rv = 0#Receiver number
	timeout = 0#variable que va a medir los tiempos de espera para mandar solicitudes. 
	ventana = listaCircular()
	bandera = True;#Mientras la bandera este en true el programa va a esperar recibir paquetes.
	direccionIPDelEmisor#La direccion ip del emisor. 
	puertoDelCliente#Puerto del cliente :). 
	#estoy generando un servidor con sockets. 
	UDP_PORT
	mi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#(Por defecto utiliza tcp y ipv4)Nos genera un nuevo socket con los valores por default
	mi_socket.bind(('',int(UDP_PORT)))#Recibe dos valores que uno es el host y el otro el puerto en el que va a estar esuchando.
	mensajeNuevo = False 
	def recibir():#Capa de comunicacion. 
		while bandera: 
			paqueteRecibido, direccionIPDelEmisor = mi_socket.recvfrom(516)#Capturamos el datos y tambien la direccion del emisor.
			datosBytes = paqueteRecibido[1:3]#extraemos el numero de paquete. 
			int.from_bytes(datosBytes, byorder='big')
			if rv == datosBytes:#Si es igual al numero de paquete que estamos esperando. 
				almacenar(paqueteRecibido[4:])#se lo debemos pasar a almacenar.
				ventana.establecerInicio(rv)#Establecemos el nuevo inicio de la lista. 
				paquete = ventana.getElemento(rv)
				while paquete != -1 #Mientras el elemento que se quiera este en la lista.
					almacenar(paquete[4:])#Le mandamos los bytes de la imagen. 
					ventana.establecerInicio(rv#Establecemos el nuevo inicio de la lista. 
	
				mensajeNuevo = True#Se comunican a traves de banderas...  
			
			else:#lo guardamos en el buffer. 
				datosBytes = paqueteRecibido[1:3]
				int.from_bytes(datosBytes, byorder='big')
				if rv + 10 > datosBytes#Si esta dentro de la ventana, lo guardamos. 
					ventana.insertar(paqueteRecibido, datosBytes)
					
	def almacenar(datos):#Capa superior
		imagen = open("laImagen.jpg", "bw")#Abrimos archivo donde vamos a guardar la imagen. 
		if datos[0] = '*':#Podemos hacer que retorne un False en lugar de jugar con esa variable global. 
			bandera = False#Para la ejecucion. 
		else:
			imagen.write(datos)
			rv++ 
	
	def confirmacionDeRecepcion():#Se encarga de enviar los ACK's 
		while bandera:#Cuando el ciclo de recibir termine este tambien. 
			tiempoInicio = time()
			if mensajeNuevo#Si se recibio un mensaje con el rv que se estaba esperando, se activa la bandera. 
				mensaje = armarMensajeACK()
				mi_socket.sendto(mensaje,(direccionIPDelEmisor, int(port)))
			tiempoTotal = time() - tiempoInicio
			timeout(tiempoTotal)#Revisamos el timeout. 
			
	def timeout(tiempo): #Se que lo mas probable es que no lo hagamos con un hilo por separado... ideas? 
		if tiempo > timeout:#Si el tiempo es mayor al time out debe enviar un paquete de recepcion
			mi_socket.sendto(
			mensaje = armarMensajeACK()
			mi_socket.sendto(ack,(direccionIPDelEmisor, int(port)))#Falta que capturemos cual puero vamos a implementar. 

	def armarMensajeACK():
		ack[0] = 1#Establecemos que es un mesaje de RV. 
		numeroDePaquete = rv 
		ack[1:3] = numeroDePaquete.tobytes(3, byteorder='big')#Pasamos el numero a bytes
		return ack 
		
	
	
	
	
	
	
	
	
	
	