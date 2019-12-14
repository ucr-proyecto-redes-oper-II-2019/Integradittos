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
 
