# blueNode.py

import os
import os.path
import shutil

from threading import Lock
from tcpl.tcpl import TCPL # en carpeta inferior
from AssemblePackagesFactory import AssemblePackageFactory
from processSystem import ProcessSystem

class BlueNode:

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
        self._tcpl.startService(self.myPort)
    
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
            print("3. Ver estado de los procesos.")
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
                    sendProcessToGreen(processName, routes)
                    pass
                else:
                    print ("Por favor revise las rutas e intente de nuevo.")
                
            elif option is 2:
                pass
            elif option is 3:
                pass
            else: # option is 4:
                pass

    def sendProcessToGreen(self, processName, filesRoutes):
        # Creamos un mensaje de solicitud de enviar proceso a verde
        message = bytearray(MESSAGE_MAX_SIZE)
        message[0:4] = random.randrange(self.MAX_RANDOM)
        message[4:6] = bytearray(2)  # 0
        message[6] = self.SEND_PROCESS
        message[7:9] = bytearray(2)  # sin prioridad
        message[9:11] = int(10).to_bytes(2, byteorder='big') # TTL irrelevante
        message[11:13] = bytearray(2) # sin fuente
        message[13:15] = int(self._greenNum).to_bytes(2, byteorder='big')
        # Agregamos el nombre del proceso y los archivos que necesita
        message[15:75] = processName.encode()
        message[75:125] = filesRoutes[0].encode() # el primero es el ejecutable
        # Enviamos la solicitud
        self._tcpl.sendPackage(tableMessage, ip, port)
        # Esperamos la respuesta
        print("Esperando respuesta del verde...")
        answer = self._tcpl.receivePackage()
        # Si la respuesta es positiva, el verde activó trans confiable
        if answer[15] == 1:
            self._processSystem.sendProcess\
            (processName, filesRoutes, self._greenIp, self._greenPort, self._ownPort)
            print("Proceso enviado.")
        else:
            print("Error: El nodo verde se niega a recibir el archivo.")


node = BlueNode(2, "255.255.255.0", 10000, 10001)
node.menu()
