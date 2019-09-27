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
DATA_MAX_SIZE = 516
sn = 0#Send number
rv = 0#Receiver number
timeout = 0#variable que va a medir los tiempos de espera para mandar solicitudes.
ventana = listaCircular()
bandera = True#Mientras la bandera este en true el programa va a esperar recibir paquetes.
direccion_ip_del_emisor = ""#La direccion ip del emisor.
puerto_cliente = ""#Puerto del cliente :).
#estoy generando un servidor con sockets.
mensajeNuevo = False
candado_critico = threading.Lock
def recibir():#Capa de comunicacion.
	while bandera:
		paquete_recibido, direccion_ip_del_emisor = mi_socket.recvfrom(516)#Capturamos el datos y tambien la direccion del emisor.
		datos_bytes = paquete_recibido[1:3]#extraemos el numero de paquete.
		int.from_bytes(datos_bytes, byteorder='big')
		if rv == datos_bytes:#Si es igual al numero de paquete que estamos esperando.
			almacenar(paquete_recibido[4:])#se lo debemos pasar a almacenar.
			rv += 1
			paquete = ventana.getElemento(rv)
			while paquete != -1: #Mientras el elemento que se quiera este en la lista.
				almacenar(paquete[4:])#Le mandamos los bytes de la imagen.
				rv += 1
			mensajeNuevo = True#Se comunican a traves de banderas...
			ventana.establecerInicio(rv)#Establecemos el nuevo inicio de la lista.
		else:#lo guardamos en el buffer.
			datos_bytes = paqueteRecibido[1:3]
			int.from_bytes(datos_bytes, byteorder='big')
			if rv + 10 > datos_bytes > rv:  #Si esta dentro de la ventana, lo guardamos.
				ventana.insertar(paquete_recibido, datos_bytes)

def almacenar(datos):#Encargado de guardar el archivo(Capa superior).
	imagen = open(nombreDelArchivo, "bw")#Abrimos archivo donde vamos a guardar la imagen.
	if datos[0] == '*':#Podemos hacer que retorne un False en lugar de jugar con esa variable global.
		bandera = False #Para la ejecucion.
	else:
		imagen.write(datos)

def confirmacionDeRecepcion():#Se encarga de enviar los ACK's
	while bandera:#Cuando el ciclo de recibir termine este tambien.
		tiempo_inicio = time()
		if mensajeNuevo:#Si se recibio un mensaje con el rv que se estaba esperando, se activa la bandera.
			candado_critico.acquire()#Empezamos zona critica
			mensaje = armarMensajeACK()
			mi_socket.sendto(mensaje,(direccion_ip_del_emisor, int(port)))
			mensaje_nuevo = False
			candado_critico.release()#Fin de la zona critica.
		tiempo_total = time() - tiempo_inicio
		timeout(tiempo_total)#Revisamos el timeout.

def timeout(tiempo):
	if tiempo > timeout:#Si el tiempo es mayor al time out debe enviar un paquete de recepcion
		mensaje = armarMensajeACK()
		mi_socket.sendto(ack,(direccion_ip_del_emisor, int(port)))#Falta que capturemos cual puero vamos a implementar.

def armarMensajeACK():#Metodo que arma los mensajes.
	ack = bytearray(DATA_MAX_SIZE)
	ack[0] = 1#Establecemos que es un mesaje de RV.
	numeroDePaquete = rv
	ack[1:3] = numeroDePaquete.tobytes(3, byteorder='big')#Pasamos el numero a bytes
	return ack


# Ejecucion del programa	
UDP_PORT = input("Escriba el numero de puerto: ")
mi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#(Por defecto utiliza tcp y ipv4)Nos genera un nuevo socket con los valores por default
mi_socket.bind(('',int(UDP_PORT)))#Recibe dos valores que uno es el host y el otro el puerto en el que va a estar esuchando.
nombre_del_archivo = "laImagen.jpg"





