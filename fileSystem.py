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

		# Number for the next file/ file fragment
		self.fileCounter = 1000

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
	def storeFile (self, fileName, fileData):
		# hex returns a string that starts with "0x", so remove those characters.
		hexadecimalName = hex(self.fileCounter)[2:]

		# Get the path to which the new file will be stored.
		internalFileName = self.fullDirName + "/" + hexadecimalName + self.FILE_EXTENSION

		# Create, open, write to, and close the file 
		newFile = open(internalFileName, "wb")
		newFile.write(fileData)
		newFile.close()

		# Increases the file counter so the next one may not use the same internal fileName
		self.fileCounter += 1
		
		# Add the file to the table.
		self.fileTable[fileName] = internalFileName
	

	'''
	Recupera un archivo.
	'''
	def loadFile (self, fileName):
		pass
		#newFile = open(self.fileTable[fileName])
		#return 

	'''
	Elimina un archivo.
	'''
	def deleteFile (self, fileName):
		pass
		
	'''
	Determina si un archivo se encuentra en el sistema.
	'''
	def findFile(self, fileName):
		return fileName in self.fileTable
	
	'''
	Almacena un fragmento de archivo.
	'''
	def storeFragment (self, fileName, fragmentNo, fragmentData):
		# hex returns a string that starts with "0x", so remove those characters.
		hexadecimalName = hex(self.fileCounter)[2:]

		# Get the path to which the new fragment will be stored.
		internalFileName = self.fullDirName + "/" + hexadecimalName + self.FILE_EXTENSION

		# Create, open, write to, and close the file to store the fragment
		newFile = open(internalFileName, "wb")
		newFile.write(fragmentData)
		newFile.close()

		# Increases the file counter so the next one may not use the same internal fileName
		self.fileCounter += 1
		
		# Add the fragment to the table.
		if fileName in self.fragmentsTable:
			self.fragmentsTable[fileName][fragmentNo] = internalFileName
		else:
			self.fragmentsTable[fileName] = { fragmentNo : internalFileName }
		
	
	'''
	Recupera un diccionario con los fragmentos de un archivo, indexados según su número
	de fragmento.
	'''
	def loadFragments (self, fileName):
		if fileName in self.fragmentsTable:
			return self.fragmentsTable[fileName].copy()
		else:
			return {}
		
	'''
	Determina si algún fragmento de un archivo se encuentra en el sistema.
	'''
	def findFragment(self, fileName):
		return fileName in self.fragmentsTable

	'''
	Elimina un fragmento de archivo.
	'''
	def deleteFragment (self, fileName):
		pass