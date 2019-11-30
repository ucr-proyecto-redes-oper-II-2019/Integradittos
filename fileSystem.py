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
		if fileName in self.fileTable:
			# Obtiene el nombre interno del archivo solicitado, revisando la tabla
			# de archivos, y abre dicho archivo.
			newFile = open(self.fileTable[fileName], "rb")
			# Lee los datos del archivo
			fileData = bytearray(newFile.read())
			
			return fileData
		else:
			return bytearray()

	'''
	Elimina un archivo.
	'''
	def deleteFile (self, fileName):
		if fileName in self.fileTable:
			# Obtiene el nombre interno del archivo solicitado, revisando la tabla
			# de archivos.
			internalName = self.fileTable[fileName]
			# Elimina el archivo con el nombre encontrado
			os.remove(internalName)
			# Elimina el archivo de la tabla de archivos
			self.fileTable.pop(fileName)
		
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
		# Si hay algún fragmento del archivo solicitado,
		if fileName in self.fragmentsTable:
			# Crea un diccionario vacío
			fragments = {}

			# Para cada fragmento almacenado de ese archivo,
			for fragmentNumber, internalName in self.fragmentsTable[fileName].values():
				# Se abre y se leen los datos del fragmento
				internalFile = open(internalName, "rb")
				data = internalFile.read()

				# Y se guarda el número de fragmento como llave y los datos del fragmento
				# como valor en el diccionario para retornar
				fragments[fragmentNumber] = bytearray(data)
			
			# Retorna el diccionario con el número y los datos de cada fragmento.
			return fragments

		# Si no hay fragmentos de ese archivo,
		else:
			# Retorna un diccionario vacío
			return {}
		
	'''
	Determina si algún fragmento de un archivo se encuentra en el sistema.
	'''
	def findFragment(self, fileName):
		return fileName in self.fragmentsTable

	'''
	Elimina los fragmentos de un archivo.
	'''
	def deleteFragment (self, fileName):
		# Si hay algún fragmento del archivo solicitado,
		if fileName in self.fragmentsTable:

			# Para cada fragmento almacenado de ese archivo,
			for fragmentNumber, internalName in self.fragmentsTable[fileName].values():
				# Se eliminan los datos del fragmento
				os.remove(internalName)

				# Se elimina el fragmento de la tabla
				self.fragmentsTable.pop(fragmentNumber)
			
			# También se elimina la entrada de la tabla que indicaba la existencia
			# de fragmentos de un archivo
			self.fragmentsTable.pop(fileName)
