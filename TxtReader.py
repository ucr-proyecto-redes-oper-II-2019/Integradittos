class TxtReader:

    def readTxt(self, ruta):
        contenido = " "
        archivo = open(ruta, "r")
        for linea in archivo.readlines():
            contenido += linea + '\n'
        return contenido
