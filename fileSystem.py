# fileSystem.py

# For directory creation
import os

# For removing non-empty directories 
import shutil

# For locks
from threading import Lock

'''
Clase que administra los archivos para un nodo verde. En el sistema operativo real, los
almacena en el directorio "./<greenNodeFiles>/<nodeIdentifier>/"
Segura para uso de múltiples hilos.
'''
class FileSystem:
	_BASE_FILE_DIRECTORY = "greenNodeFiles"
	_FILE_EXTENSION = ".dat"

	'''
	Constructor de objetos de clase FileSystem.
	'''
	def __init__(self, nodeIdentifier):
		# Identificador. (Para almacenar los archivos en el sistema real.)
		self._id = nodeIdentifier
		# Diccionario con los nombres internos de archivos, indexados por sus nombres reales.
		self._fileTable = {}
		# Diccionario donde las llaves corresponden a los nombres reales de los archivos
		# a los que pertenecen los fragmentos, y los valores son diccionarios de los datos
		# de los fragmentos indexados por sus números de fragmento.
		self._fragmentsTable = {}

		# Directory in the real OS where file data is put
		self._fullDirName = "./" + FileSystem._BASE_FILE_DIRECTORY + "/" + str(nodeIdentifier)

		# Number for the next file/ file fragment
		self._fileCounter = 1000

		# Crea el directorio para almacenar archivos
		if not os.path.exists(self._fullDirName):
			os.makedirs(self._fullDirName)
		# Candado para multihilos
		self.lock = Lock()


	'''
	Destructor de objetos de clase FileSystem.
	(Utilizar para limpiar todo rastro de archivos en la computadora usada)
	'''
	def __del__(self):
		shutil.rmtree(self._fullDirName)


	'''
	Almacena un archivo.
	'''
	def storeFile (self, fileName, fileData):
		# hex returns a string that starts with "0x", so remove those characters.
		hexadecimalName = hex(self._fileCounter)[2:]

		# Get the path to which the new file will be stored.
		internalFileName = self._fullDirName + "/" + hexadecimalName + self._FILE_EXTENSION

		# Lock critical section
		self.lock.acquire()

		# Create, open, write to, and close the file 
		newFile = open(internalFileName, "wb")
		newFile.write(fileData)
		newFile.close()

		# Increases the file counter so the next one may not use the same internal fileName
		self._fileCounter += 1
		
		# Add the file to the table.
		self._fileTable[fileName] = internalFileName

		# Unlock critical section
		self.lock.release()
	

	'''
	Recupera un archivo.
	'''
	def loadFile (self, fileName):
		returnData = 0
		
		# Lock critical section
		self.lock.acquire()
		if fileName in self._fileTable:
			# Obtiene el nombre interno del archivo solicitado, revisando la tabla
			# de archivos, y abre dicho archivo.
			newFile = open(self._fileTable[fileName], "rb")
			# Lee los datos del archivo
			fileData = bytearray(newFile.read())
			
			returnData = fileData
		else:
			returnData = bytearray()
		# Unock critical section
		self.lock.release()

		return returnData

	'''
	Elimina un archivo.
	'''
	def deleteFile (self, fileName):
		# Lock critical section
		self.lock.acquire()

		if fileName in self._fileTable:
			# Obtiene el nombre interno del archivo solicitado, revisando la tabla
			# de archivos.
			internalName = self._fileTable[fileName]
			# Elimina el archivo con el nombre encontrado
			os.remove(internalName)
			# Elimina el archivo de la tabla de archivos
			self._fileTable.pop(fileName)
		
		# Unlock critical section
		self.lock.release()
		
	'''
	Determina si un archivo se encuentra en el sistema.
	'''
	def findFile(self, fileName):
		# Lock critical section
		self.lock.acquire()

		answer = fileName in self._fileTable

		# Unlock critical section
		self.lock.release()

		return answer
	
	'''
	Almacena un fragmento de archivo.
	'''
	def storeFragment (self, fileName, fragmentNo, fragmentData):
		# hex returns a string that starts with "0x", so remove those characters.
		hexadecimalName = hex(self._fileCounter)[2:]

		# Get the path to which the new fragment will be stored.
		internalFileName = self._fullDirName + "/" + hexadecimalName + self._FILE_EXTENSION

		# Lock critical section
		self.lock.acquire()

		# Create, open, write to, and close the file to store the fragment
		newFile = open(internalFileName, "wb")
		newFile.write(fragmentData)
		newFile.close()

		# Increases the file counter so the next one may not use the same internal fileName
		self._fileCounter += 1
		
		# Add the fragment to the table.
		if fileName in self._fragmentsTable:
			self._fragmentsTable[fileName][fragmentNo] = internalFileName
		else:
			self._fragmentsTable[fileName] = { fragmentNo : internalFileName }
		
		# Unlock critical section
		self.lock.release()
		
	
	'''
	Recupera un diccionario con los fragmentos de un archivo, indexados según su número
	de fragmento.
	'''
	def loadFragments (self, fileName):
		returnData = {}

		# Lock critical section
		self.lock.acquire()

		# Si hay algún fragmento del archivo solicitado,
		if fileName in self._fragmentsTable:
			# Crea un diccionario vacío
			fragments = {}

			# Para cada fragmento almacenado de ese archivo,
			for fragmentNumber, internalName in self._fragmentsTable[fileName].items():
				# Se abre y se leen los datos del fragmento
				internalFile = open(internalName, "rb")
				data = internalFile.read()

				# Y se guarda el número de fragmento como llave y los datos del fragmento
				# como valor en el diccionario para retornar
				fragments[fragmentNumber] = bytearray(data)
			
			# Retorna el diccionario con el número y los datos de cada fragmento.
			returnData = fragments

		# Unlock critical section
		self.lock.release()

		return returnData
		
	'''
	Determina si algún fragmento de un archivo se encuentra en el sistema.
	'''
	def findFragment(self, fileName):
		# Lock critical section
		self.lock.acquire()

		answer = fileName in self._fragmentsTable

		# Unlock critical section
		self.lock.release()

		return answer

	'''
	Elimina los fragmentos de un archivo.
	'''
	def deleteFragment (self, fileName):
		# Lock critical section
		self.lock.acquire()

		# Si hay algún fragmento del archivo solicitado,
		if fileName in self._fragmentsTable:

			# Para cada fragmento almacenado de ese archivo,
			for internalName in self._fragmentsTable[fileName].values():
				# Se eliminan los datos del fragmento
				os.remove(internalName)
			
			# Se eliminan los fragmentos del archivo en la tabla
			self._fragmentsTable.pop(fileName)
		
		# Unlock critical section
		self.lock.release()
