# fileSystemTests.py
from fileSystem import FileSystem

# Function for testing the FileSystem class
def testFileSystem():
    fs1 = FileSystem(11)
    fs2 = FileSystem(13)

    fileA = [bytearray("Hola, mundo. ", 'utf-8'), bytearray("Soy una prueba. ", 'utf-8'), bytearray("Adiós, mundo.", 'utf-8')]
    fileB = bytearray("Sabías que a los dioses de la muerte les gustan las manzanas?", 'utf-8')
    fileC = bytearray("Tendría que analizarlo", 'utf-8')
    fileD = [bytearray(3), bytearray(2), bytearray(1)]


    fs1.storeFile("B", fileB)
    fs1.storeFile("C", fileC)
    i = 0
    for fragment in fileA:
        fs1.storeFragment("A", i, fragment)
        i += 1
    i = 0
    for fragment in fileD:
        fs1.storeFragment("D", i, fragment)
        i += 1

    fs2.storeFile("B", fileB)
    i = 0
    for fragment in fileA:
        fs2.storeFragment("A", i, fragment)
        i += 1

    assert fs1.findFile("A") == False, "A must not be found in filesystem 1."
    assert fs1.findFragment("A") == True, "A's pieces must be found in filesystem 1."
    assert fs1.findFile("B") == True, "B must be found in filesystem 1."
    assert fs1.findFragment("B") == False, "B's pieces must not be found in filesystem 1."
    assert fs1.findFile("C") == True, "C must be found in filesystem 1."
    assert fs1.findFragment("C") == False, "C's pieces must not be found in filesystem 1."
    assert fs1.findFile("D") == False, "D must not be found in filesystem 1."
    assert fs1.findFragment("D") == True, "D's pieces must be found in filesystem 1."

    assert fs2.findFragment("A") == True, "A's pieces must be found in filesystem 2."
    assert fs2.findFile("B") == True, "B must be found in filesystem 2."
    assert fs2.findFile("C") == False, "C must not be found in filesystem 2."
    assert fs2.findFragment("D") == False, "D's pieces must not be found in filesystem 2."


    aRecoveredFrom2 = fs2.loadFragments("A")
    bRecoveredFrom2 = fs2.loadFile("B")

    fs2.deleteFragment("A")
    fs2.deleteFile("B")
    
    assert fs2.findFragment("A") == False, "A's pieces must not be found in filesystem 2."
    assert fs2.findFile("B") == False, "B must not be found in filesystem 2."

    del fs2


    aRecoveredFrom1 = fs1.loadFragments("A")
    bRecoveredFrom1 = fs1.loadFile("B")
    cRecoveredFrom1 = fs1.loadFile("C")
    dRecoveredFrom1 = fs1.loadFragments("D")

    fs1.deleteFragment("A")
    fs1.deleteFile("B")

    assert fs1.findFragment("A") == False, "A's pieces must not be found in filesystem 1."
    assert fs1.findFile("B") == False, "B must not be found in filesystem 1."
    assert fs1.findFile("C") == True, "C must be found in filesystem 1."
    assert fs1.findFragment("D") == True, "D's pieces must be found in filesystem 1."

    assert len(aRecoveredFrom2) == 3, "Filesystem 2 must have all 3 pieces of A."
    assert aRecoveredFrom2[0] == fileA[0], "First piece of A has changed in filesystem 2."
    assert aRecoveredFrom2[1] == fileA[1], "Second piece of A has changed in filesystem 2."
    assert aRecoveredFrom2[2] == fileA[2], "Third piece of A has changed in filesystem 2."

    assert bRecoveredFrom2 == fileB, "B changed in filesystem 2."



    assert len(aRecoveredFrom1) == 3, "Filesystem 1 must have all 3 pieces of A."
    assert aRecoveredFrom1[0] == fileA[0], "First piece of A has changed in filesystem 1."
    assert aRecoveredFrom1[1] == fileA[1], "Second piece of A has changed in filesystem 1."
    assert aRecoveredFrom1[2] == fileA[2], "Third piece of A has changed in filesystem 1."

    assert bRecoveredFrom1 == fileB, "B changed in filesystem 1."
    assert cRecoveredFrom1 == fileC, "C changed in filesystem 1."

    assert len(dRecoveredFrom1) == 3, "Filesystem 1 must have all 3 pieces of D."
    assert dRecoveredFrom1[0] == fileD[0], "First piece of D has changed in filesystem 1."
    assert dRecoveredFrom1[1] == fileD[1], "Second piece of D has changed in filesystem 1."
    assert dRecoveredFrom1[2] == fileD[2], "Third piece of D has changed in filesystem 1."



# Runs the testing if this is the main module
if __name__ == "__main__":
    testFileSystem()
    #assert False, "This assert is set to be always false."
