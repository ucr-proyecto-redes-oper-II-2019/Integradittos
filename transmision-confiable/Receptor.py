import socket
import threading
import threading 
import sys 
import select
import ctypes #para el memset
import time
import listaCircular
from time import time

#Fabian e Isaac.

class Receptor:
	DATA_MAX_SIZE = 516
	sn = 0#Send number  
	rv = 0#Receiver number
	timeout = 0#variable que va a medir los tiempos de espera para mandar solicitudes. 
	ventana = listaCircular()
	bandera = True#Mientras la bandera este en true el programa va a esperar recibir paquetes.
	direccion_ip_del_emisor = ""#La direccion ip del emisor.
	puerto_cliente = ""#Puerto del cliente :).
	#estoy generando un servidor con sockets. 
	UDP_PORT = ""
	mi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#(Por defecto utiliza tcp y ipv4)Nos genera un nuevo socket con los valores por default
	mi_socket.bind(('',int(UDP_PORT)))#Recibe dos valores que uno es el host y el otro el puerto en el que va a estar esuchando.
	mensaje_nuevo = False
	nombre_del_archivo = "laImagen.jpg"


	def _init__(self):

	def recibir(self):#Capa de comunicacion.
		while self.bandera:
			paquete_recibido, self.direccion_ip_del_emisor = self.mi_socket.recvfrom(516)#Capturamos el datos y tambien la direccion del emisor.
			datos_bytes = paquete_recibido[1:3]#extraemos el numero de paquete.
			int.from_bytes(datos_bytes, byteorder='big')
			if self.rv == datos_bytes:#Si es igual al numero de paquete que estamos esperando.
				self.almacenar(paquete_recibido[4:])#se lo debemos pasar a almacenar.
				self.rv += 1
				self.ventana.establecerInicio(self.rv)#Establecemos el nuevo inicio de la lista.
				paquete = self.ventana.getElemento(self.rv)
				while paquete != -1: #Mientras el elemento que se quiera este en la lista.
					self.almacenar(paquete[4:])#Le mandamos los bytes de la imagen.
					self.rv += 1
					self.ventana.establecerInicio(self.rv)#Establecemos el nuevo inicio de la lista.
				mensajeNuevo = True#Se comunican a traves de banderas...
			else:#lo guardamos en el buffer. 
				datos_bytes = self.paqueteRecibido[1:3]
				int.from_bytes(datos_bytes, byteorder='big')
				if self.rv + 10 > datos_bytes > self.rv:  #Si esta dentro de la ventana, lo guardamos.
					self.ventana.insertar(paquete_recibido, datos_bytes)
					
	def almacenar(self, datos):#Encargado de guardar el archivo(Capa superior).
		imagen = open(self.nombreDelArchivo, "bw")#Abrimos archivo donde vamos a guardar la imagen.
		if datos[0] == '*':#Podemos hacer que retorne un False en lugar de jugar con esa variable global.
			self.bandera = False #Para la ejecucion.
		else:
			imagen.write(datos)
	
	def confirmacionDeRecepcion(self):#Se encarga de enviar los ACK's
		while self.bandera:#Cuando el ciclo de recibir termine este tambien.
			tiempo_inicio = time()
			if self.mensajeNuevo:#Si se recibio un mensaje con el rv que se estaba esperando, se activa la bandera.
				mensaje = self.armarMensajeACK()
				self.mi_socket.sendto(mensaje,(self.direccion_ip_del_emisor, int(self.port)))
			tiempo_total = time() - tiempo_inicio
			self.timeout(tiempo_total)#Revisamos el timeout.
			
	def timeout(self, tiempo):
		if tiempo > self.timeout:#Si el tiempo es mayor al time out debe enviar un paquete de recepcion
			mensaje = self.armarMensajeACK()
			self.mi_socket.sendto(self.ack,(self.direccion_ip_del_emisor, int(self.port)))#Falta que capturemos cual puero vamos a implementar.

	def armarMensajeACK(self):#Metodo que arma los mensajes.
		ack = bytearray(self.DATA_MAX_SIZE)
		ack[0] = 1#Establecemos que es un mesaje de RV.
		numeroDePaquete = self.rv
		ack[1:3] = numeroDePaquete.tobytes(3, byteorder='big')#Pasamos el numero a bytes
		return ack 
		
	
	
	
	
	
	
	
	
	
	