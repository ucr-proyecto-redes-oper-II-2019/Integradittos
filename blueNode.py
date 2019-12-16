# blueNode.py

import os
import os.path
import shutil
import random
import sys

from threading import Lock
from tcpl.tcpl import TCPL # en carpeta inferior
from AssemblePackagesFactory import AssemblePackageFactory
from processSystem import ProcessSystem

class BlueNode:

    MESSAGE_MAX_SIZE = 1015
    MAX_RANDOM = 65000
    SEND_PROCESS = 50
    RUN_PROCESS = 51
    ASK_FOR_PROCESS = 52
    PROCESS_OUTPUT = 53

    def __init__(self, greenNum, greenIp, greenPort, ownPort):
        self._greenId = greenNum
        self._greenIp = greenIp
        self._greenPort = greenPort # TCPL
        self._greenReliTransPort = greenPort + 1000
        self._ownPort = ownPort
        self._processSystem = ProcessSystem(ownPort, False)
        self._tcpl = TCPL()
        self._tcpl.startService(self._ownPort)

    '''
    def start(self):
        pass

    def runInterface(self):
        pass
    '''

    def displayMenuOptions(self):
        print("\n\n # # #   # # #   # # #  Nodo azul  # # #   # # #  # # # \n")
        num = -1
        while True:
            print("1. Enviar un programa.")
            print("2. Ejecutar un programa.")
            print("3. Preguntar el estado de un proceso.")
            print("4. Salir.")

            try:
                num = int(input("\nSeleccione una opción: "))
                if 0 < num and num < 5:
                    break

            except ValueError:
                pass

            print("\nPor favor seleccione una opción válida.\n")

        return num

    def menu(self):
        option = 0
        while option is not 4:
            option = self.displayMenuOptions()

            if option is 1:
                print ("\n\n # # # Envío de un programa # # #")
                processName = input ("Ingrese el nombre del proceso que quiere enviar al nodo verde:\n")
                print ("Ingrese la ruta del archivo ejecutable que desea correr, seguido por")
                print ("las rutas de los demás archivos necesarios para la ejecución, separadas")
                print ("por espacios.")
                routes = input("\nArchivos: ")
                print ("\n")
                routes = routes.split()

                # Remove a linebreak if it exists:
                if routes[-1][-1] is '\n':
                    routes[-1] = routes[-1][:-1]

                allFound = True
                for route in routes:
                    if not os.path.isfile(route):
                        allFound = False
                        print ("Archivo", route, "no fue encontrado...")

                if allFound:
                    # Run the program sender
                    self.sendProcessToGreen(processName, routes)
                    pass
                else:
                    print ("Por favor revise las rutas e intente de nuevo.")

            elif option is 2:
                pName = input("Ingrese el nombre del proceso a ejecutar: ")
                self.sendExecutionToGreen(pName)
            elif option is 3:
                pName = input("Ingrese el nombre del proceso a consultar: ")
                self.askForProcessToGreen(pName)
            else: # option is 4:
                pass

    def sendProcessToGreen(self, processName, filesRoutes):
        # Creamos un mensaje de solicitud de enviar proceso a verde
        message = bytearray(self.MESSAGE_MAX_SIZE)
        message[0:4] = int(random.randrange(self.MAX_RANDOM)).to_bytes(4, byteorder='big')
        message[4:6] = bytearray(2)  # 0
        message[6] = self.SEND_PROCESS
        message[7:9] = bytearray(2)  # sin prioridad
        message[9:11] = int(10).to_bytes(2, byteorder='big') # TTL irrelevante
        message[11:13] = bytearray(2) # sin fuente
        message[13:15] = int(self._greenId).to_bytes(2, byteorder='big')
        # Agregamos el nombre del proceso y los archivos que necesita
        message[15:75] = processName.encode()
        message[75:125] = filesRoutes[0].encode() # el primero es el ejecutable
        print("Proceso:", processName, ", ejecutable:", filesRoutes)
        # Enviamos la solicitud
        self._tcpl.sendPackage(message, self._greenIp, self._greenPort)
        # Esperamos la respuesta
        print("Esperando respuesta del verde...")
        answer, ipPort = self._tcpl.receivePackage()
        # Si la respuesta es positiva, el verde activó trans confiable
        if answer[15] == 1:
            self._processSystem.sendProcess\
            (processName, filesRoutes, self._greenIp, self._greenPort, self._ownPort)
            print("Proceso enviado.")
        else:
            print("Error: El nodo verde se niega a recibir el archivo.")

    def sendExecutionToGreen(self, processName):
        # Creamos un mensaje de solicitud de enviar proceso a verde
        message = bytearray(self.MESSAGE_MAX_SIZE)
        message[0:4] = int(random.randrange(self.MAX_RANDOM)).to_bytes(4, byteorder='big')
        message[4:6] = bytearray(2)  # 0
        message[6] = self.RUN_PROCESS
        message[7:9] = bytearray(2)  # sin prioridad
        message[9:11] = int(10).to_bytes(2, byteorder='big') # TTL irrelevante
        message[11:13] = bytearray(2) # sin fuente
        message[13:15] = int(self._greenId).to_bytes(2, byteorder='big')
        # Agregamos el nombre del proceso y los archivos que necesita
        message[15:75] = processName.encode()
        # Enviamos la solicitud
        self._tcpl.sendPackage(message, self._greenIp, self._greenPort)
        # Esperamos la respuesta
        print("Esperando respuesta del verde...")
        answer, ipPort = self._tcpl.receivePackage()
        print("El proceso:", processName, "se mandó a ejecutar.")

    def askForProcessToGreen(self, processName):
        # Creamos un mensaje de solicitud de enviar proceso a verde
        message = bytearray(self.MESSAGE_MAX_SIZE)
        message[0:4] = int(random.randrange(self.MAX_RANDOM)).to_bytes(4, byteorder='big')
        message[4:6] = bytearray(2)  # 0
        message[6] = self.ASK_FOR_PROCESS
        message[7:9] = bytearray(2)  # sin prioridad
        message[9:11] = int(10).to_bytes(2, byteorder='big') # TTL irrelevante
        message[11:13] = bytearray(2) # sin fuente
        message[13:15] = int(self._greenId).to_bytes(2, byteorder='big')
        # Agregamos el nombre del proceso y los archivos que necesita
        message[15:75] = processName.encode()
        # Enviamos la solicitud
        self._tcpl.sendPackage(message, self._greenIp, self._greenPort)
        # Esperamos la respuesta
        print("Esperando respuesta del verde...")
        answer, ipPort = self._tcpl.receivePackage()
        # Si la respuesta es positiva, el verde activó trans confiable
        if answer[15] == 0:
            print("\n***El programa", processName, "no ha sido ejecutado***\n")
        elif answer[15] == 1:
            print("El programa", processName, " esta corriendo***\n")
        elif answer[15] == 2:
            print("\n***El programa", processName, " ya terminó***\n")
        else:
            print("\n***El programa", processName, " no se encuentra en el nodo verde***\n")

# id nodo verde, ip verde, puerto verde, puerto propio
node = BlueNode(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
node.menu()
