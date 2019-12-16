# blueNode.py

import os
import os.path
import shutil
from threading import Lock

class BlueNode:

    def __init__(self, greenIp, greenPort, ownPort):
        self._greenIp = greenIp
        self._greenPort = greenPort # TCPL
        self._greenReliTransPort = greenPort + 1000
        self._ownPort = ownPort
        #self._processSystem = ProcessSystem(grennIp, greenPort, ownPort)
        
    def start(self):
        pass

    def runInterface(self):
        pass

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
                    # here
                    # and erase these comments
                    # please
                    # :)
                    pass
                else:
                    print ("Por favor revise las rutas e intente de nuevo.")
                
            elif option is 2:
                pass
            elif option is 3:
                pass
            else: # option is 4:
                pass


node = BlueNode("255.255.255.0", 10000, 10001)
node.menu()