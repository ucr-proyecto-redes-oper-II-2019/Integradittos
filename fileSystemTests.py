# fileSystemTests.py
from fileSystem import FileSystem

# Function for testing the FileSystem class
def testFileSystem():
    fs1 = FileSystem(11)
    fs2 = FileSystem(13)

    fileAFragments = [bytearray("Hola, mundo. ", 'utf-8'), bytearray("Soy una prueba. ", 'utf-8'), bytearray("Adiós, mundo.", 'utf-8')]
    fileB = bytearray("Sabías que a los dioses de la muerte les gustan las manzanas?", 'utf-8')
    fileC = bytearray("Tendría que analizarlo", 'utf-8')
    fileD = [bytearray(3), bytearray(2), bytearray(1)]

    fs1.


# Runs the testing if this is the main module
if __name__ == "__main__":
    testFileSystem()
