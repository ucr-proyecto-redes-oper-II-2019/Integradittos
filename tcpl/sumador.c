#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>
#include "suma.h"

#define MAX_LINEA 2048
#define MIN(a,b) ( (a) > (b) ? (b) : (a) )

void leer_array(FILE * archivo, int * arreglo, int * cant_elementos)
{
	char * linea;
	size_t size = MAX_LINEA;
	getline(&linea, &size, archivo);
	linea[strcspn(linea, "\n")] = 0;
	char *pt;
    pt = strtok (linea,",");
    *cant_elementos = atoi(pt);
    pt = strtok (NULL, ",");
    int contador_elementos = 0;
    while (pt != NULL) 
    {
        arreglo[contador_elementos++] = atoi(pt);
        pt = strtok (NULL, ",");
    }
    //return contador_elementos;
}
    


int sumar_vector(int * vector, int elementos)
{
	size_t thread_count = omp_get_max_threads();

	int resultados[elementos]; 
	int sumas_de_vectores = 0;
	int cantidad_sumas = 0;
	if( elementos % 2 == 0 )
	{
		sumas_de_vectores = elementos / 2;
		cantidad_sumas = elementos / 2;
	}
	else
	{
		sumas_de_vectores = elementos / 2 + 1;
		cantidad_sumas = elementos / 2 + 1;
	}

	memcpy(resultados, vector, elementos * sizeof(int));
	
	int cantidad_elementos = cantidad_sumas;
	for(int i = 0; i < sumas_de_vectores; i++)
	{ 	
		printf("Cantidad de sumas en iteracion %d: %d\n", i, cantidad_sumas );
		int temporal[cantidad_sumas];

		thread_count = MIN(thread_count, cantidad_sumas);
		#pragma omp parallel for num_threads(thread_count) shared(resultados, temporal, cantidad_elementos)
		for(int j = 0; j < cantidad_sumas; j++)
		{
			if( j == cantidad_sumas - 1 && cantidad_elementos % 2 == 1 )
			{
				printf("Hilo %d baja: %d\n", omp_get_thread_num(),resultados[j*2]);
				temporal[j] = resultados[j*2];
			}
			else
			{	
				printf("Hilo %d suma: %d con %d\n", omp_get_thread_num(),resultados[j*2], resultados[j*2+1] );
				temporal[j] = suma(resultados[j*2], resultados[j*2+1]);
			}
		}
		memcpy(resultados, temporal, cantidad_sumas * sizeof(int));
		cantidad_elementos = cantidad_sumas;
		printf("La proxima sumatoria tendrá: %d elementos\n", cantidad_elementos);
		if( cantidad_sumas % 2 == 0 )
			cantidad_sumas /= 2;
		else
			cantidad_sumas = (cantidad_sumas / 2) + 1;

		
	}
	return resultados[0];
}

int main(int argc, char* argv[])
{
	FILE * archivo;
 	// int threads = atoi(argv[1]);
 	if( argc > 1)
 	{
 		archivo = fopen(argv[1], "rb");
 		if(archivo == NULL)
 		{
 			printf("No se encontro archivo: %s\n", argv[0]);
 		}
 	}
 	else
 	{
 		printf("Uso: ./sumar archivo.txt\n");
 	}	
 		
	int * vectorInicial;
	int cantidad_elementos = 0;
	leer_array(archivo, vectorInicial, &cantidad_elementos);
	
	int resultado = sumar_vector(vectorInicial,cantidad_elementos);
	printf("%d\n", resultado);
	fclose(archivo);
	return 0;
}
