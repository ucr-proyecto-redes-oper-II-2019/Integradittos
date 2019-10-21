#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


#define F_NAME_SIZE 255

/*
 *
 */
int pack_process(long file_count, char * file_names[], FILE * archivo_proceso)
{
	// El primer campo del archivo con para reanudar el proceso
	// es la cantidad de archivos a enviar
	fwrite(&file_count, sizeof(long), 1, archivo_proceso);

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
		fwrite(file_names[index], sizeof(char),F_NAME_SIZE, archivo_proceso);
		fwrite(&file_size, sizeof(long), 1, archivo_proceso);
		// Se escribe el archivo byte por byte (podría ser mas eficiente
		// con aritmetica modular)
		char one_byte;
		for(size_t byte; byte < file_size; ++byte)
		{
			fread(&one_byte, sizeof(char), 1, file);
			fwrite(&one_byte, sizeof(char), 1, archivo_proceso);
		}

		fclose(file);
	}

	return 0;
}

/*
 *
 */
int unpack_process(FILE * archivo_proceso)
{
	return 0;
}