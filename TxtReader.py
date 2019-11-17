class TxtReader:

    def readTxt(self, ruta=".txt"):
        contenido = " "
        archivo = open(ruta, "r")
        for linea in archivo.readlines():
            contenido += linea + '\n'
        return contenido
