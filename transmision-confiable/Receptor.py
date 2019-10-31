import socket
import threading
import sys 
import select
import ctypes #para el memset
import time
from listaCircular import listaCircular

#Fabian e Isaac.
DATA_MAX_SIZE = 516
sn = 0#Send number
rv = 0#Receiver number
tiempoFuera = 0.3#variable que va a medir los tiempos de espera para mandar solicitudes.
ventana = listaCircular()
nombre_del_archivo = "archivo_recibido"
bandera = True#Mientras la bandera este en true el programa va a esperar recibir paquetes.
banderaFinalizar = False
direccion_ip_del_emisor = ""#La direccion ip del emisor.
puerto_cliente = ""#Puerto del cliente :).
#estoy generando un servidor con sockets.
mensajeNuevo = False

if len(sys.argv) != 3:
	print("Uso: python3 Receptor.py puerto nombre_archivo")
	sys.exit()

nombre_del_archivo = sys.argv[2]
UDP_PORT = sys.argv[1]
mi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#(Por defecto utiliza tcp y ipv4)Nos genera un nuevo socket con los valores por default
mi_socket.bind(('', int(UDP_PORT)))#Recibe dos valores que uno es el host y el otro el puerto en el que va a estar esuchando.
#direccion, puerto = mi_socket.

imagen = open(nombre_del_archivo, "bw")#Abrimos archivo donde vamos a guardar la imagen.

def recibir():#Capa de comunicacion.
	global rv
	global bandera
	global direccion_ip_del_emisor
	global mensajeNuevo
	global ventana
	while bandera:
		paquete_recibido, direccion_ip_del_emisor = mi_socket.recvfrom(516)#Capturamos el datos y tambien la direccion del emisor.
		datos_bytes = paquete_recibido[1:4]#extraemos el numero de paquete.
		datos_bytes = int.from_bytes(datos_bytes, byteorder='big')
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
			datos_bytes = paquete_recibido[1:4]
			enteroBytes = int.from_bytes(datos_bytes, byteorder='big')
			if rv + 10 > enteroBytes > rv:  #Si esta dentro de la ventana, lo guardamos.
				ventana.insertar(paquete_recibido, enteroBytes)

def almacenar(datos):#Encargado de guardar el archivo(Capa superior).
	global nombre_del_archivo
	global imagen
	global bandera
	global banderaFinalizar
	if datos[0] == 42 and datos[1] == 0:#Podemos hacer que retorne un False en lugar de jugar con esa variable global.
		print("Recibimos un asterisco rv= % d " %(rv))
		banderaFinalizar = True #Para la ejecucion.
		imagen.close()
	else:
		imagen.write(datos)
	

def confirmacionDeRecepcion():#Se encarga de enviar los ACK's
	global bandera
	global direccion_ip_del_emisor
	global banderaFinalizar 
	#global candado_critico
	candado_critico = threading.Lock()
	global mensajeNuevo
	while bandera:#Cuando el ciclo de recibir termine este tambien.
		tiempo_inicio = time.time()
		if mensajeNuevo:#Si se recibio un mensaje con el rv que se estaba esperando, se activa la bandera.
			candado_critico.acquire()#Empezamos zona critica
			mensaje = armarMensajeACK()
			mi_socket.sendto(mensaje, direccion_ip_del_emisor)
			mensajeNuevo = False
			candado_critico.release()#Fin de la zona critica.
		if banderaFinalizar:
			bandera = False 
		 	
		tiempo_total = time.time() - tiempo_inicio
		timeout(tiempo_total)#Revisamos el timeout.

def timeout(tiempo):
	global tiempoFuera
	if tiempo > tiempoFuera:#Si el tiempo es mayor al time out debe enviar un paquete de recepcion
		mensaje = armarMensajeACK()
		mi_socket.sendto(mensaje, direccion_ip_del_emisor)#Falta que capturemos cual puero vamos a implementar.

def armarMensajeACK():#Metodo que arma los mensajes.
	global rv
	global DATA_MAX_SIZE
	ack = bytearray(DATA_MAX_SIZE)
	ack[0] = 0x01#Establecemos que es un mesaje de RV.
	numeroDePaquete = rv
	print("Enviando el ack: % d " %(numeroDePaquete))
	ack[1:4] = numeroDePaquete.to_bytes(3, byteorder='big')#Pasamos el numero a bytes
	return ack

#Definimos los hilos principales.
hilo_de_recepcion = threading.Thread(target=recibir)
hilo_de_confirmacion_de_recepcion = threading.Thread(target=confirmacionDeRecepcion)

# Ejecucion del programa	


#Iniciamos los hilos
hilo_de_recepcion.start()
hilo_de_confirmacion_de_recepcion.start() 

hilo_de_recepcion.join()#Hilo principal
#hilo_de_confirmacion_de_recepcion.join()
