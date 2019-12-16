# fileSystem.py

# For directory creation
import os

# For removing non-empty directories 
import shutil

# For locks
from threading import Lock

# subprocess.popen()
import subprocess


class ProcessSystem:


    _BASE_FILE_DIRECTORY = "greenNodeProcesses"

    '''Inicializa el objeto con se respectivo puerto y un booleano subPath,
    si subPath es True, el ProcessSystem recibe archivos en sub directorios'''
    def __init__(self, ownPort, subPath):
        # nombre (key) | ruta concantenado [0] | ruta ejecutable [1] | ruta arch salida [2] | finalizado [3](v,f)
        self._processList = dict()
        self._ownerNode = -1
        self._savingPath = "./" + ProcessSystem._BASE_FILE_DIRECTORY + "/" + str(ownPort) + "/"
        if subPath:
            if not os.path.exists(self._savingPath):
                os.makedirs(self._savingPath)
        ''' Esto pertenece al nodo, no al servicio
        self._ownPort = ownPort
        self._tcplPort = TCPLPort 
        self._reliTransPort = TCPLPort + 1000
        self._greenIp = greenIp
        '''
        

    '''Recibe el proceso con ese nombre (programName) por transmisión confiable'''
    def receiveProcess(self, programName, executableName, port):

        reliTransPort = int(port) + 1000
        processDirectory = self._savingPath + programName + "/"
        print("Creando carpeta:", processDirectory)
        # Crear la carpeta para el proceso
        os.makedirs(processDirectory, exist_ok=True)
        
        # Agregamos el proceso a la lista
        self._processList[programName] = [processDirectory + programName, processDirectory + executableName, processDirectory + programName + "_output.txt", False]

        # Recibimos el programa por transmisión confiable
        # Creamos el comando para recibir proceso con syscall
        programPath = processDirectory #+ "/" + programName
        recvComand = "./recibir_proceso" + " " + str(reliTransPort) + " " + programPath + " " + programName
        print(recvComand)
        os.system(recvComand)


    '''Envia un proceso'''
    def sendProcess(self, programName, filesList, ip, destPort, ownPort):

        destPort = int(destPort) + 1000
        ownPort = int(ownPort) + 1000
        # Creamos el comando para enviar por transmisión confiable
        sendComand = "./enviar_proceso " + ip + " " + str(destPort) + " " + str(ownPort) + " " + programName + " "
        for file in filesList:
            sendComand = sendComand + file + " "
        print(sendComand)
        os.system(sendComand)

    '''Ejecuta un proceso, debería correrse en otro hilo para que sea esperado'''        
    def executeProcess(self, programName):
        
        # Buscamos el proceso en la lista
        if  not programName in self._processList:
            return 0
        else:
            ''' Usando fork '''
            '''
            # Se crea un subproceso para ejecutar el programa
            pid = os.fork()
            if pid is 0:
                os.system(self._processList[0][1]) # ver processList en __init__()
            else:
                os.wait()
            '''

            ''' Usando sub procesos python: https://docs.python.org/2/library/subprocess.html '''

            # Archivo de salida
            # archivo output, ver processList en __init__()
            output = open(self._processList[programName][2], "w") 

            # ejecutable y output, ver processList en __init__()
            process = subprocess.Popen(self._processList[programName][1], stdout=output) 

            process.wait()

            # Determinamos que el proceso ya terminó su ejecución
            self._processList[programName][3] = True
            print("Proceso:", programName, "terminó.")


    def isProcessDone(self, programName):
        # Si el proceso esta en el sistema
        if programName in self._processList:
            # Si terminó retornamos 1
            if self._processList[programName][3]:
                return 1
            # sino, retornamos 0
            else:
                return 0
        # sino, retornamos 2 (para evitar manipular negativos en bytes)
        else:
            return 2
    
        
