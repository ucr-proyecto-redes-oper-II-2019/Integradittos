# fileSystem.py

# For directory creation
import os

# For removing non-empty directories 
import shutil

# For locks
from threading import Lock


class ProcessSystem:


    _BASE_FILE_DIRECTORY = "greenNodeProcesses"

    def __init__(self, greenIp, TCPLPort, ownPort):
        # nombre (key) | ruta concantenado [0] | ruta ejecutable [1]
        self._processList = dict()
        self._ownerNode = -1
        self._savingPath = "./" + ProcessSystem._BASE_FILE_DIRECTORY + "/" + str(ownPort) + "/"
        if not os.path.exists(self._savingPath):
            os.makedirs(self._savingPath)
        self._ownPort = ownPort
        self._tcplPort = TCPLPort 
        self._reliTransPort = TCPLPort + 1000
        self._greenIp = greenIp
        

    '''Recibe el proceso con ese nombre (programName) por transmisión confiable'''
    def receiveProcess(self, programName, executableName):

        processDirectory = self._savingPath + programName + "/"
        print("Creando carpeta:", processDirectory)
        # Crear la carpeta para el proceso
        os.makedirs(processDirectory)
        
        # Agregamos el proceso a la lista
        self._processList[programName] = [processDirectory + programName, processDirectory + executableName]

        # Recibimos el programa por transmisión confiable
        # Creamos el comando para recibir proceso con syscall
        programPath = processDirectory #+ "/" + programName
        comando = "./recibir_proceso" + " " + str(self._reliTransPort) + " " + programPath + " " + programName
        print(comando)
        os.system(comando)


    '''Envia un proceso'''
    def sendProcess(self, programName, filesList):

        # Creamos el comando para enviar por transmisión confiable
        comando = "./enviar_proceso " + self._greenIp + " " + self._reliTransPort + " " + self._ownPort + " "
        for file in filesList:
            comando = comando + file + " "
        print(comando)

        
    def executeProcess(self, programName)

        # Buscamos el proceso en la lista
        if  not programName in self._processList:
            return 0
        else:
            # Se crea un subproceso para ejecutar el programa
            pid = os.fork()
            if pid is 0:
                os.system(self._processList[0][1])
            else:
                os.wait()
        return 1

    def sendProcessToRun(self):
        pass
        
    
        
