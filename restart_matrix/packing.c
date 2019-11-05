#include <libgen.h> // para basename()
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Constantes para el número de bytes en los campos 
#define F_NAME_SIZE 64
#define N_FILE_SIZE sizeof(int)
#define FILE_BYTES_SIZE sizeof(int)


/*
 * Ejecuta un comando para otorgar permiso de ejecución al programa
 * @param file_name nombre del archivo.
 */
int exec_privilege(char * file_name)
{
	char comando[512];
	strcpy(comando, "chmod u+x ./");
   	strcat(comando, file_name);
   	
   	printf("%s\n", comando);

	// Invocamos el comando para enviar el archivo
	int sys_error = system(comando);

	if( sys_error == -1 )
	{
		printf("No existe el archivo ejecutable.\n");
		return -1;
	}
	
	return 0;
}

/*
 * Concatena los archivos dados en file_names en uno solo
 * @param file_count cantidad de archivos a concetenar
 * @param flne_names arreglo con lo nombres del archivo
 * #param archivo_proceso file descriptor del archivo con la concatenación
 */
int pack_process(long file_count, char * file_names[], FILE * archivo_proceso)
{
	// El primer campo del archivo con para reanudar el proceso
	// es la cantidad de archivos a enviar
	fwrite(&file_count, N_FILE_SIZE, 1, archivo_proceso);

	// Los campos siguientes son archivos, con el formato:
	// nombre (255B) | tamaño X en Bytes (8B) | archivo (X B)
	// (el primer archivo DEBE ser el ejecutable)
	FILE * file;
	size_t file_size = 0;
	for (int index = 0; index < file_count; ++index)
	{
		// Se intenta abrir el archivo
		printf("Abriendo archivo: %s\n", file_names[index]);
		file = fopen(file_names[index], "rb");
		if( file == NULL ) {
			perror("Error abriendo archivo: ");
			return(-1);
		}

		// Se obtiene el tamaño en bytes
		fseek(file, 0L, SEEK_END);
		file_size = ftell(file);
		rewind(file);

		// Se escriben: nombre, tamaño y archivo
		char * file_base_name = basename(file_names[index]);
		fwrite(file_base_name, sizeof(char),F_NAME_SIZE, archivo_proceso);
		fwrite(&file_size, FILE_BYTES_SIZE, 1, archivo_proceso);
		printf("Se empaquetó %s: %ld bytes\n", file_base_name, file_size);
		// Se escribe el archivo byte por byte (podría ser mas eficiente
		// con aritmetica modular)
		//char one_byte;
		//for(size_t byte; byte < file_size; ++byte)
		//{
		//	fread(&one_byte, sizeof(char), 1, file);
		//	fwrite(&one_byte, sizeof(char), 1, archivo_proceso);
		//}
		char file_data[file_size];
		fread(file_data, sizeof(char), file_size, file);
		fwrite(file_data, sizeof(char), file_size, archivo_proceso);

		fclose(file);
	}
	return 0;
}

/*
 *Metodo que "Desempaca" informacion de un archivo. 
 *@param archivo_proceso Archivo que contiene informacion concatenada.
 */
int unpack_process(FILE * archivo_proceso)
{
	long cantidad_de_archivos = 0;
	long cantidad_de_bytes_archivo = 0; 
	char nombre_del_archivo[F_NAME_SIZE];
	FILE * file; 

	//Leemos la cantidad de archivos el primer long que hay en el archivo, que es el numero de archivos que hay 
	fread(&cantidad_de_archivos, N_FILE_SIZE, 1, archivo_proceso);
	printf("Cantidad de archivos recibidos: %ld\n", cantidad_de_archivos);
	for(int indice = 0; indice < cantidad_de_archivos; indice++)
	{
		//Leemos el nombre del archivo. 
		fread(nombre_del_archivo, sizeof(char), F_NAME_SIZE, archivo_proceso); 
		//Leemos la cantidad de bytes que pesa el archivo.
		fread(&cantidad_de_bytes_archivo, FILE_BYTES_SIZE, 1, archivo_proceso);
		printf("Desempaquetando %s: %ld bytes\n", nombre_del_archivo, cantidad_de_bytes_archivo);
		//Abrimos el archivo. 
		file = fopen(nombre_del_archivo, "wb");
		//Pasamos los datos al archivo.
		//char one_byte;
		//for(size_t byte; byte < cantidad_de_bytes_archivo; ++byte)
		//{
		//	fread(&one_byte, sizeof(char), 1, archivo_proceso);
		//	fwrite(&one_byte, sizeof(char), 1, file);
		//}
		char file_data[cantidad_de_bytes_archivo];
		fread(file_data, sizeof(char), cantidad_de_bytes_archivo, archivo_proceso);
		fwrite(file_data, sizeof(char), cantidad_de_bytes_archivo, file); 
		
		fclose(file);
		
		// 	Si se desempaquetó l primer archivo, se da permisos de ejecución al ejecutable (primer archivo)
		// pues es el ejecutable
		if(indice == 0)
			exec_privilege(nombre_del_archivo);
	}	
	return 0;
}

