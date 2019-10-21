/*
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "packing.h"

int main(int argc, char* argv[])
{
	if( argc < 4)
	{
		printf("Uso: ./enviar_proceso [nombre_proceso] [ejecutable] archivo1 archivo2 ...\n");
		return -1;
	}

	FILE * archivo_proceso;

	// Se intenta abrir el archivo que contendrá
	// lo necesario para restartear el proceso
	archivo_proceso = fopen(argv[1], "wb");
	if( archivo_proceso == NULL ) {
		perror("Error abriendo archivo: ");
		return(-1);
	}

	// Se compilan todos los archivos indicados en archivo_proceso
	int error = pack_process(argc - 2 /*./enviar nombre ...*/, argv + 2 , archivo_proceso);

	fclose(archivo_proceso);

	if( error )
	{
		printf("Error: no se pudo reunir los archivos necesarios\n");
		return -1;
	}
	else
	{
		// Enviar proceso usando transmision confiable (quiza haga falta 
		// hacer que transmision confiable reciba por argumentos la información)

		// Usar esto para llamar el programa de Python:
		// https://www.geeksforgeeks.org/system-call-in-c/
	}

	return 0;

}