# fileSystem.py

# For directory creation
import os

# For removing non-empty directories 
import shutil

# For locks
from threading import Lock


class ProcessSystem:


    _BASE_FILE_DIRECTORY = "greenNodeProcesses"

    def __init__(self, id, port):
        # nombre | ejecutable |
        self._processList = dict()
        self._ownerNode = -1
        self._savingPath = "./" + ProcessSystem._BASE_FILE_DIRECTORY + "/" + str(id)
        if not os.path.exists(self._savingPath):
            os.makedirs(self._savingPath)
        self._reliTransPort = port

    def receiveProcess(self, programName, executableName):


        processDirectory = self._savingPath + "/" + programName
        print("Creando carpeta:", processDirectory)
        # Crear la carpeta para el proceso
        os.makedirs(processDirectory)
        
        # Cambiamos de directorio
        #os.chdir(processDirectory)

        # Recibimos el programa por transmisión confiable
        # Creamos el comando para recibir proceso con syscall
        programPath = processDirectory + "/" #+ programName
        comando = "./recibir_proceso" + " " + str(self._reliTransPort + 1000) + " " + programPath + " " + programName
        print(comando)
        os.system(comando)

        os.system(programPath + executableName)
        
    def sendProcess(self, )
        