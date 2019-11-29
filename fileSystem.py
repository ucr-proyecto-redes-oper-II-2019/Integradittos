# fileSystem.py

# For directory creation
import os

# For removing non-empty directories 
import shutil

'''
Clase que administra los archivos para un nodo verde. En el sistema operativo real, los
almacena en el directorio "./<greenNodeFiles>/<nodeIdentifier>/"
'''
class FileSystem:
	BASE_FILE_DIRECTORY = "greenNodeFiles"
	FILE_EXTENSION = ".dat"

	'''
	Constructor de objetos de clase FileSystem.
	'''
	def __init__(self, nodeIdentifier):
		# Identificador. (Para almacenar los archivos en el sistema real.)
		self.id = nodeIdentifier
		# Diccionario con los nombres de archivos en el sistema de archivos, junto con un identificador.
		self.fileTable = {}
		# Diccionario con los nombres de los fragmentos en el sistema de archivos, junto con un identificador.
		self.fragmentsTable = []

		# Directory in the real OS where file data is put
		self.fullDirName = "./" + FileSystem.BASE_FILE_DIRECTORY + "/" + nodeIdentifier

		# Crea el directorio para almacenar archivos
		if not os.path.exists(self.fullDirName):
			os.makedirs(self.fullDirName)


	'''
	Destructor de objetos de clase FileSystem.
	(Utilizar para limpiar todo rastro de archivos en la computadora usada)
	'''
	def __del__(self):
		shutil.rmtree(self.fullDirName)


	'''
	Almacena un archivo.
	'''
	def storeFile (self, fileName, data):
		pass
	
	'''
	Recupera un archivo.
	'''
	def loadFile (self, fileName):
		pass
		
	'''
	Determina si un archivo se encuentra en el sistema.
	'''
	def findFile(self, fileName):
		pass
	
	'''
	Almacena un fragmento de archivo.
	'''
	def storeFragment (self, fragmentName, data):
		pass
	
	'''
	Recupera un fragmento de archivo.
	'''
	def loadFragment (self, fragmentName):
		pass
		
	'''
	Determina si un archivo se encuentra en el sistema.
	'''
	def findFragment(self, fileName):
		pass
	
	#todo: determinar si estos dos metodos son necesarios:
	#def listFiles(self):
	#def listFragments(self):
		
