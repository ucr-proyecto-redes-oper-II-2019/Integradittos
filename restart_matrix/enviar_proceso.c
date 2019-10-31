/*
 * Proyecto Integrados Redes/Oper II 2019 UCR
 * Ejemplo de transmisión de archivos (enviar)
 * Grupo Integradittos
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "packing.h"

int main(int argc, char* argv[])
{
	if( argc < 3)
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
		// Se piden los datos de envío
		char ip_receptor[16];
		char puerto_receptor[6];
		char puerto_local[6];
		printf("Ingrese: IP-receptor Puerto_receptor Puerto_local\n");
		scanf("%s %s %s", ip_receptor, puerto_receptor, puerto_local);

		// Ensamblamos el comando para enviar el archivo del proceso
		char comando[1024];
		strcpy(comando, "python3 Emisor.py ");
	   	strcat(comando, ip_receptor);
	   	strcat(comando, " ");
	   	strcat(comando, puerto_receptor);
	   	strcat(comando, " ");
	   	strcat(comando, argv[1]);
	   	strcat(comando, " ");
	   	strcat(comando, puerto_local);

	   	printf("%s\n", comando);

		// Invocamos el comando para enviar el archivo
		int sys_error = system(comando);

		if( sys_error == -1 )
		{
			printf("Hubo un error enviando el archivo.\n");
			return -1;
		}
	}

	return 0;

}