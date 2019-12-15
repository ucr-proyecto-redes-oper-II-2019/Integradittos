/*
 * Proyecto Integrados Redes/Oper II 2019 UCR
 * Ejemplo de transmisión de archivos (recibir)
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
		printf("Uso: ./recibir_proceso [puerto] [ruta_archivo] [nombre_archivo]\n");
		return -1;
	}

	// Se pide el puerto usado para recibir el archivo del proceso
	char * puerto_local = argv[1];
	char * ruta_archivo = argv[2];
	char * nombre_archivo = argv[3];
	//printf("Ingrese: Puerto_local nombre_archivo\n");
	//scanf("%s %s", puerto_local, nombre_archivo);

	// Ensamblamos el comando para enviar el archivo del proceso
	char comando[1024];
	strcpy(comando, "python3 Receptor.py ");
   	strcat(comando, puerto_local);
   	strcat(comando, " ");
   	strcat(comando, ruta_archivo);

   	printf("%s\n", comando);

	// Invocamos el comando para enviar el archivo
	int sys_error = system(comando);

	if( sys_error == -1 )
	{
		printf("Hubo un error recibiendo el archivo.\n");
		return -1;
	}

	FILE * archivo_proceso;

	// Se intenta abrir el archivo que contiene
	// los archivos necesarios para restartear el proceso
	char nombre[100];
	strcpy(nombre, ruta_archivo);
	strcat(nombre, nombre_archivo);
	archivo_proceso = fopen(nombre, "rb");
	if( archivo_proceso == NULL ) {
		perror("Error abriendo archivo: ");
		return(-1);
	}

	// Se desempaquetan los archivos recividos
	int error = unpack_process(archivo_proceso, ruta_archivo);

	fclose(archivo_proceso);

	if( error )
	{
		printf("Error: no se pudo desempaquetar el proceso\n");
		return -1;
	}

	return 0;

}