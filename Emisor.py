import socket 
import threading 
import sys 
import select
import ctypes
import time
import os.path
from listaCircular import listaCircular

# General
DATA_MAX_SIZE = 1 + 3 + 512
BUFFER_SIZE = 10
BUFFER_START = 0

# Para envio
# en segundos
SEND_TIMEOUT = 3 
# ventana
SENDING_BUFFER = listaCircular()
# bus para enviar las partes de la imagen a capa inferior
SENDING_BUS = bytearray(512) 
# contador de mensajes en el buffer
SENDING_BUFFER_COUNT = 0 
# mutex del buffer
SN_max = 0
SENDING_BUFFER_LOCK = threading.Lock() 
SN_min = 0
#FINAL_MESSAGE = generar_mensaje_final()
# se vuelve True al leer toda la imagen
end_of_image = False 
# se vuelve true al enviar todas las partes de la imagen con exito
sending_complete = False 
# indica si hay una porcion de la imagen en el bus
bytes_on_bus = False 
# variable usada para determinar cual es el numero de secuencia del ACK final
finishing_ACK = 0 
# tiempo en segundos que el emisor va a esperar un ACK
receiver_timeout = 10

def cargar_imagen(archivo):
    global end_of_image
    # abrir imagen
    print("Emisor: abriendo", archivo)
    in_file = open(archivo, "rb")
    # insertamos el nombre del archivo en el primer slice
    image_slice = bytearray(512)
    image_slice[0:50] = os.path.basename(archivo.encode())
    image_slice[50:512] = in_file.read(462)
    # Mientras no se haya leido toda la imagen
    while not end_of_image:   
        # si no hay mas que leer, es el final
        if not image_slice:
            # "libera" el bus para que la capa inferior pueda enviar el paquete con el *
            end_of_image = True
        else:
        	# si no, se envia la seccion normal
            enviar_seccion(image_slice)
        # se lee el siguiente slice
        image_slice = in_file.read(512)
    in_file.close()

def enviar_seccion(image_slice):
    global SENDING_BUS
    global bytes_on_bus
    # pone la porcion de la imagen en el bus
    SENDING_BUS = image_slice
    # espera a que la capa inferior tome la porcion que esta en el bus
    bytes_on_bus = True
    while bytes_on_bus:
        time.sleep(.2)

def sending_buffering():
    global SN_max
    global SN_min
    global SENDING_BUFFER_COUNT
    global BUFFER_SIZE
    global SENDING_BUS
    global SENDING_BUFFER_LOCK
    global bytes_on_bus
    global finishing_ACK
    SENDING_BUFFER.establecer_inicio(BUFFER_START)
    while not end_of_image:
        # si SN_max es mayor o igual al mensaje que falta de ACK (SN_min),
        # y hay espacio en el buffer
        # y hay bytes en el bus
        if SN_max >= SN_min and SENDING_BUFFER_COUNT < BUFFER_SIZE and bytes_on_bus:
            # 0 000 0...
            mensaje_por_enviar = bytearray(DATA_MAX_SIZE)
            # setea el encabezado
            mensaje_por_enviar[0] = 0
            mensaje_por_enviar[1:4] = SN_max.to_bytes(3, byteorder='big')
	        # copia la porcion de la imagen en el mensaje
            mensaje_por_enviar[4:4+512] = SENDING_BUS
            SENDING_BUFFER_LOCK.acquire() # region critica
            # guarda el mensaje en el buffer
            SENDING_BUFFER.insertar(mensaje_por_enviar, SN_max)
            # aumentamos el SN_max y el contador del buffer
            SN_max += 1
            SENDING_BUFFER_COUNT += 1
            SENDING_BUFFER_LOCK.release() # region critica
            bytes_on_bus = False

    # se inserta el mensaje final que contiene el *
    mensaje_final = bytearray(DATA_MAX_SIZE)
    mensaje_final[0] = 0
    mensaje_final[1:4] = SN_max.to_bytes(3, byteorder='big')
    fin_de_imagen = bytearray(512)
    fin_de_imagen[0] = 42 # un *
    mensaje_final[4:4+512] = fin_de_imagen
    finishing_ACK = SN_max
    print("Inserté paquete final (Sn = % d)" %(SN_max))
    SENDING_BUFFER_LOCK.acquire() # region critica
    SENDING_BUFFER.insertar(mensaje_final, SN_max)
    SN_max += 1
    SENDING_BUFFER_LOCK.release() # region critica

def enviar_imagen(ip, port):
    global SN_max
    global SN_min
    global DATA_MAX_SIZE
    global SENDING_BUFFER_LOCK
    global sending_complete
    # 0 000 0...
    mensaje_por_enviar = bytearray(DATA_MAX_SIZE)
    # empaquetar establecer conexión
    #mensaje_por_enviar[0] = 0
    #mensaje_por_enviar[1:3] = bytearray({0,0,0})
    #enviar paquete
    #mi_socket.sendto(mensaje_por_enviar,(ip, int(port)))
    #esperar ACK para el "handshake"
    #ACK, addr = mi_socket.recvfrom(DATA_MAX_SIZE)
    #print("Handshake!")
    while not sending_complete:
    	# en caso de que el hilo que recive ACK actualice el SN_min, lo podamos notar
        last_SN_min = SN_min
        # rangos de la ventana
        iterador_ventana = SN_min
        final_ventana = SN_max
        # inicio (y reinicio) del timer
        timeout = time.time() + SEND_TIMEOUT   # en segundos
        # mientras no se haya acabado el timeout de envio y no hayan señales de vida del receptor (ACK)
        while time.time() < timeout and last_SN_min == SN_min:
        	SENDING_BUFFER_LOCK.acquire() # region critica
        	if(iterador_ventana < final_ventana):
        		#print("Enviando paquete: % d" %(iterador_ventana))
        		mi_socket.sendto(SENDING_BUFFER.get_elemento(iterador_ventana), (ip, int(port)))
        		iterador_ventana += 1
        	SENDING_BUFFER_LOCK.release() # region critica

        	'''
            SENDING_BUFFER_LOCK.acquire() # region critica
            for msg in range (SN_min, SN_max):
                # podria acabarse el timeout de envio y o recibir un ACK mientras se envian los paquetes
                #if time.time() < timeout and last_SN_min == SN_min:
                mi_socket.sendto(SENDING_BUFFER.get_elemento(msg), (ip, int(port)))
            SENDING_BUFFER_LOCK.release() # region critica
            '''

def recibir_ACK():
    global SENDING_BUFFER
    global DATA_MAX_SIZE
    global SN_min
    global sending_complete
    global SENDING_BUFFER_COUNT
    global finishing_ACK
    ultimo_ACK = -1
    while not sending_complete:
        ACK = bytearray(512)
        addr = 0
        # el socket tiene un timeout en segundos, si no hay respuesta, se termina el envío
        try:
            ACK, addr = mi_socket.recvfrom(DATA_MAX_SIZE)
        except socket.error as e:
            error = e
            print(error)
            print("No hay respuesta del receptor")
            sending_complete = True

        # se toma el num de secuencia del mensaje
        SN_min = int.from_bytes(ACK[1:4], byteorder='big')
        print("Recibi ACK: % d" %(SN_min))
        # si es un ack del asterisco, se completo el envio
        if end_of_image and SN_min >= finishing_ACK:
            sending_complete = True
        # si el nuevo SN_min es diferente al ultimo, actualizamos el inicio de la ventana
        if(ultimo_ACK < SN_min):
        	if(ultimo_ACK != -1):
        		SENDING_BUFFER.establecer_inicio(SN_min)
        		SENDING_BUFFER_COUNT -= (SN_min - ultimo_ACK)
        	ultimo_ACK = SN_min  

# Ejecucion del programa

if len(sys.argv) != 5:
	print("Uso: python3 Emisor.py IP_destino Puerto_destino archivo Puerto_local")
	sys.exit()

UDP_PORT = sys.argv[4]
mi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#(Por defecto utiliza tcp y ipv4)Nos genera un nuevo socket con los valores por default
mi_socket.bind(('',int(UDP_PORT)))#Recibe dos valores que uno es el host y el otro el puerto en el que va a estar esuchando.
# socket non blocking
mi_socket.settimeout(receiver_timeout)

#ipPortFile = input("Ingrese: IP Puerto archivo: ") #lee una linea
#ipPortFileLine = ipPortFile.split() #split a la linea

ip = sys.argv[1]
port = sys.argv[2]
archivo = sys.argv[3]

# Threads
hilo_de_carga_de_archivo = threading.Thread(target=cargar_imagen, args=(archivo,))
hilo_de_buffering = threading.Thread(target=sending_buffering) 	
hilo_de_envio = threading.Thread(target=enviar_imagen, args=(ip,port,))
hilo_de_recibir_ACK = threading.Thread(target=recibir_ACK)

hilo_de_carga_de_archivo.start()
hilo_de_buffering.start()
hilo_de_recibir_ACK.start()
hilo_de_envio.start()

hilo_de_carga_de_archivo.join()
hilo_de_buffering.join()
hilo_de_recibir_ACK.join()
hilo_de_envio.join()

