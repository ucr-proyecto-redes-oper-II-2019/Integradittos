import socket 
import threading 
import sys 
import select
import ctypes
import time
from listaCircular import listaCircular

# General
DATA_MAX_SIZE = 1 + 4 + 512
BUFFER_SIZE = 10
BUFFER_START = 0

# Para envio
SEND_TIMEOUT = 3 # en segundos
SENDING_BUFFER = listaCircular() #buffer
SENDING_BUS = bytearray(512) # bus para enviar las partes de la imagen a capa inferior
SENDING_BUFFER_COUNT = 0 # contador de mensajes en el buffer
SENDING_BUFFER_LOCK = threading.Lock() # mutex del buffer
SN_max = 0
SN_min = 0
#FINAL_MESSAGE = generar_mensaje_final() #se está haciendo en la capa superior por ahora
end_of_image = False # se vuelve True al leer toda la imagen
sending_complete = False # se vuelve true al enviar todas las partes de la imagen con exito
bytes_on_bus = False # indica si hay una porcion de la imagen en el buss

def cargar_imagen(archivo):
    global end_of_image
    # abrir imagen
    in_file = open(archivo, "rb")
    # Mientras no se haya leido toda la imagen
    while not end_of_image:
        image_slice = in_file.read(512)
        # si es una seccion normal, se envia
        if image_slice != '':
            enviar_seccion(image_slice)
        else:
            # si es el final de imagen se envia un *
            fin_de_imagen = bytearray(512)
            fin_de_imagen[0] = 42 # un *
            enviar_seccion(fin_de_imagen)
            end_of_image = True # se han leido todas las porciones de la imagen
    in_file.close()

def enviar_seccion(image_slice):
    global SENDING_BUS
    # pone la porcion de la imagen en el bus
    SENDING_BUS = image_slice
    # espera a que la capa inferior tome la porcion del bus
    bytes_on_bus = True
    while bytes_on_bus:
        time.wait(.3)

def sending_buffering():
    global SN_max
    global SN_min
    global SENDING_BUFFER_COUNT
    global BUFFER_SIZE
    global SENDING_BUS
    global SENDING_BUFFER_LOCK
    global bytes_on_bus
    SENDING_BUFFER.establecerInicio(BUFFER_START)
    while not end_of_image:
        # si SN_max es mayor o igual al mensaje que falta de ACK (SN_min),
        # y hay espacio en el buffer
        # y hay bytes en el bus
        if SN_max >= SN_min and SENDING_BUFFER_COUNT < BUFFER_SIZE and bytes_on_bus:
            # 0 000 0...
            mensaje_por_enviar = bytearray(DATA_MAX_SIZE)
            # setea el encabezado
            mensaje_por_enviar[0] = 0
            mensaje_por_enviar[1:3] = SN_max.to_bytes(3, byteorder='big')
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


def enviar_imagen(ip, port):
    global SN_max
    global SN_min
    global DATA_MAX_SIZE
    global SENDING_BUFFER_LOCK
    global sending_complete
    # 0 000 0...
    mensaje_por_enviar = bytearray(DATA_MAX_SIZE)
    # empaquetar establecer conexión
    mensaje_por_enviar[0] = 0
    mensaje_por_enviar[1:3] = bytearray({0,0,0})
    #enviar paquete
    mi_socket.sendto(mensaje_por_enviar,(ip, int(port)))
    #esperar ACK para el "handshake"
    ACK, addr = mi_socket.recvfrom(DATA_MAX_SIZE)

    while not sending_complete:
        last_SN_min = SN_min
        timeout = time.time() + SEND_TIMEOUT   # en segundos
        # mientras no se haya acabado el timeout de envio y no hayan señales de vida del receptor (ACK)
        while time.time() < timeout and last_SN_min == SN_min:
            SENDING_BUFFER_LOCK.acquire() # region critica
            for msg in range (SN_min, SN_max):
                # podria acabarse el timeout de envio y o recibir un ACK mientras se envian los paquetes
                #if time.time() < timeout and last_SN_min == SN_min:
                mi_socket.sendto(SENDING_BUFFER.getElemento(msg), (ip, int(port)))
            SENDING_BUFFER_LOCK.release() # region critica

def recibir_ACK():
    global DATA_MAX_SIZE
    global SN_min
    global sending_complete
    while not sending_complete:
        ACK, addr = mi_socket.recvfrom(DATA_MAX_SIZE)
        SN_min = int.from_bytes(ACK[1:4], byteorder='big')
        # si es un ack del asterisco, se completo el envio
        if (ACK[4] == 42):
            sending_complete = True

def generar_mensaje_final():
    msj_final = bytearray(DATA_MAX_SIZE)
    msj_final[4] = 42
    return msj_final

# Ejecucion del programa
UDP_PORT = input("Escriba el numero de puerto: ")
mi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#(Por defecto utiliza tcp y ipv4)Nos genera un nuevo socket con los valores por default
mi_socket.bind(('',int(UDP_PORT)))#Recibe dos valores que uno es el host y el otro el puerto en el que va a estar esuchando.
# socket non blocking
mi_socket.setblocking(0)
ipPortFile = input("IP Port file: ") #lee una linea
ipPortFileLine = ipPortFile.split() #split a la linea
ip = ipPortFileLine[0]
port = ipPortFileLine[1]
archivo = ipPortFileLine[2]

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

