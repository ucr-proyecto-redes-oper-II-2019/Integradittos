import socket
import threading
import sys
import select
import ctypes  # para el memset
import time
from listaCircular import listaCircular

# ---------------------------------------------------------------------------Definicion de varibles---------------------------------------------------------------------------------
# Variables finales.
INICIO_DE_DATOS = 4
INICIO_DE_NUMERO_SECUENCIA = 1
FIN_DE_NUMERO_SECUENCIA = 4
TAMANO_VENTANA = 10
SENAL_DE_PARADA = 42  # Es un asterizco.
POSICION_DEL_SN = 0
CANTIDAD_DE_BYTES_NUM_SECUENCIA = 3

# Fabian e Isaac.
DATA_MAX_SIZE = 516
sn = 0  # Send number
rv = 0  # Receiver number
tiempo_fuera = 0.3  # variable que va a medir los tiempos de espera para mandar solicitudes.
ventana = listaCircular()
nombre_del_archivo = "archivo_recibido"
bandera = True  # Mientras la bandera este en true el programa va a esperar recibir paquetes.
bandera_finalizar = False
direccion_ip_del_emisor = ""  # La direccion ip del emisor.
puerto_cliente = ""  # Puerto del cliente :).
# estoy generando un servidor con sockets.
mensaje_nuevo = False
# ---------------------------------------------------------------------------fin de la definicion --------------------------------------------------------------------------------------
if len(sys.argv) != 3:
    print("Uso: python3 Receptor.py puerto nombre_archivo")
    sys.exit()

nombre_del_archivo = sys.argv[2]
UDP_PORT = sys.argv[1]
mi_socket = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)  # (Por defecto utiliza tcp y ipv4)Nos genera un nuevo socket con los valores por default
mi_socket.bind(('', int(UDP_PORT)))  # Recibe dos valores que uno es el host y el otro el puerto en el que va a estar esuchando.
# direccion, puerto = mi_socket.

imagen = open(nombre_del_archivo, "bw")  # Abrimos archivo donde vamos a guardar la imagen.


def recibir():  # Capa de comunicacion.
    global rv
    global bandera
    global direccion_ip_del_emisor
    global mensaje_nuevo
    global ventana

    global DATA_MAX_SIZE
    global INICIO_DE_DATOS
    global INICIO_DE_NUMERO_SECUENCIA
    global FIN_DE_NUMERO_SECUENCIA
    global TAMANO_VENTANA

    while not bandera_finalizar:
        paquete_recibido, direccion_ip_del_emisor = mi_socket.recvfrom(
            DATA_MAX_SIZE)  # Capturamos el datos y tambien la direccion del emisor.
        datos_bytes = paquete_recibido[
                      INICIO_DE_NUMERO_SECUENCIA:FIN_DE_NUMERO_SECUENCIA]  # extraemos el numero de paquete.
        datos_bytes = int.from_bytes(datos_bytes, byteorder='big')
        if rv == datos_bytes:  # Si es igual al numero de paquete que estamos esperando.
            rv += 1
            almacenar(paquete_recibido[INICIO_DE_DATOS:])  # se lo debemos pasar a almacenar.
            paquete = ventana.get_elemento(rv)
            while paquete != -1:  # Mientras el elemento que se quiera este en la lista.
                rv += 1
                almacenar(paquete[INICIO_DE_DATOS:])  # Le mandamos los bytes de la imagen.
            mensaje_nuevo = True  # Se comunican a traves de banderas...
            ventana.establecerInicio(rv)  # Establecemos el nuevo inicio de la lista.
        else:  # lo guardamos en el buffer.
            datos_bytes = paquete_recibido[INICIO_DE_NUMERO_SECUENCIA:FIN_DE_NUMERO_SECUENCIA]
            entero_bytes = int.from_bytes(datos_bytes, byteorder='big')
            if rv + TAMANO_VENTANA > entero_bytes > rv:  # Si esta dentro de la ventana, lo guardamos.
                ventana.insertar(paquete_recibido, entero_bytes)


def almacenar(datos):  # Encargado de guardar el archivo(Capa superior).
    global SENAL_DE_PARADA  # Es un asterizco.
    global nombre_del_archivo
    global imagen
    global bandera
    global bandera_finalizar
    global candado_critico
    candado_critico.acquire()
    if datos[0] == SENAL_DE_PARADA and datos[1] == 0:  # Podemos hacer que retorne un False en lugar de jugar con esa variable global.
        print("Recibimos un asterisco rv= % d " % rv)
        bandera_finalizar = True  # Para la ejecucion.
        imagen.close()
    else:
        imagen.write(datos)
    candado_critico.release()


def confirmacion_de_recepcion():  # Se encarga de enviar los ACK's

    global bandera
    global direccion_ip_del_emisor
    global bandera_finalizar
    global candado_critico
    candado_critico = threading.Lock()
    global mensaje_nuevo
    while bandera:  # Cuando el ciclo de recibir termine este tambien.
        candado_critico.acquire()  # Empezamos zona critica
        tiempo_inicio = time.time()
        if bandera_finalizar:
            bandera = False
        if mensaje_nuevo:  # Si se recibio un mensaje con el rv que se estaba esperando, se activa la bandera.
            mensaje = armar_mensaje_ACK()
            mi_socket.sendto(mensaje, direccion_ip_del_emisor)
            mensaje_nuevo = False
        candado_critico.release()  # Fin de la zona critica.
        tiempo_total = time.time() - tiempo_inicio
        timeout(tiempo_total)  # Revisamos el timeout.


def timeout(tiempo):
    global tiempo_fuera
    if tiempo > tiempo_fuera:  # Si el tiempo es mayor al time out debe enviar un paquete de recepcion
        mensaje = armar_mensaje_ACK()
        mi_socket.sendto(mensaje, direccion_ip_del_emisor)  # Falta que capturemos cual puero vamos a implementar.


def armar_mensaje_ACK():  # Metodo que arma los mensajes.
    global DATA_MAX_SIZE
    global POSICION_DEL_SN
    global CANTIDAD_DE_BYTES_NUM_SECUENCIA
    global INICIO_DE_NUMERO_SECUENCIA
    global FIN_DE_NUMERO_SECUENCIA

    global rv
    global DATA_MAX_SIZE
    ack = bytearray(DATA_MAX_SIZE)
    ack[POSICION_DEL_SN] = 0x01  # Establecemos que es un mesaje de RV.
    numero_de_paquete = rv
    print("Enviando el ack: % d " % numero_de_paquete)
    ack[INICIO_DE_NUMERO_SECUENCIA:FIN_DE_NUMERO_SECUENCIA] = numero_de_paquete.\
        to_bytes(CANTIDAD_DE_BYTES_NUM_SECUENCIA, byteorder='big')  # Pasamos el numero a bytes
    return ack


# Definimos los hilos principales.
hilo_de_recepcion = threading.Thread(target=recibir)
hilo_de_confirmacion_de_recepcion = threading.Thread(target=confirmacion_de_recepcion)

# Ejecucion del programa	


# Iniciamos los hilos
hilo_de_recepcion.start()
hilo_de_confirmacion_de_recepcion.start()

hilo_de_recepcion.join()  # Hilo principal
# hilo_de_confirmacion_de_recepcion.join()
