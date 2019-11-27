# fileSystem.py

'''
Clase que administra los archivos para un nodo verde.
'''
class FileSystem:
	'''
	Constructor de objetos de clase FileSystem.
	'''
	def __init__(self, nodeIdentifier):
		# Identificador. (Para almacenar los archivos en el sistema real.)
		self.id = nodeIdentifier
		# Lista con los nombres de archivos en el sistema de archivos.
		self.fileTable = []
		# Lista con los nombres de los fragmentos en el sistema de archivos.
		self.fragmentsTable = []
		
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
		
