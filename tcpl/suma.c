#include <stdio.h>
#include <string.h>
#include <limits.h>
#include "suma.h"

#define MAX_CALLS 100

int suma(int x, int y)
{
	int cantidad_calls =  guardar_registro_funcion("suma");
	if( cantidad_calls > MAX_CALLS)
		return INT_MAX;
	else
		return x + y;
}

int guardar_registro_funcion(char* nombre)
{
	int size_nombre = sizeof(nombre);
	char nombre_log[size_nombre+7];  // + log.bin
	strcpy(nombre_log, nombre);
	strcat(nombre_log, "log.bin");
	int contador = 0;

	FILE * file = fopen(nombre_log, "rb");

    if (file != NULL)
    {
        int chars = fread(&contador, sizeof (contador), 1, file);
        if (chars != 0)
        {
            printf("Lei: %d\n", contador );
        }

        fclose(file);
    }

    file = fopen(nombre_log, "wb");
    ++contador;
    fwrite(&contador, sizeof (contador), 1, file);
    printf("Escribi: %d\n", contador);
    fclose(file);
}

