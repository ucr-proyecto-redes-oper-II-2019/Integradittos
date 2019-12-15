# blueNode.py

import os

import shutil

from threading import Lock

class BlueNode:

    def __init__(self, greenIp, greenPort, ownPort):
        self._greenIp = greenIp
        self._greenPort = greenPort # TCPL
        self._greenReliTransPort = greenPort + 1000
        self._ownPort = ownPort
        self._processSystem = ProcessSystem(grennIp, greenPort, ownPort)
        
    def start():
        pass

    def runInterface():
        pass

    def displayMenu(self):
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
 
