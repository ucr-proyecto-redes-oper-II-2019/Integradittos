#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>
#include "suma.h"

int sumar_vector(int * vector, int countThreads)
{
	int resultados[countThreads]; 
	int sumas_de_vectores = 0;
	int cantidad_sumas = 0;
	if( countThreads % 2 == 0 )
	{
		sumas_de_vectores = countThreads / 2;
		cantidad_sumas = countThreads / 2;
	}
	else
	{
		sumas_de_vectores = countThreads / 2 + 1;
		cantidad_sumas = countThreads / 2 + 1;
	}

	memcpy(resultados, vector, countThreads * sizeof(int));
	
	int cantidad_elementos = countThreads;
	for(int i = 0; i < sumas_de_vectores; i++)
	{ 	
		printf("Cantidad de sumas en iteracion %d: %d\n", i, cantidad_sumas );
		int temporal[cantidad_sumas];
		 
		#pragma omp parallel for num_threads(cantidad_sumas) shared(resultados)
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
 	int threads = atoi(argv[1]);
	int vectorInicial[ ] = {1,2,3,4,5};
	
	int resultado = sumar_vector(vectorInicial,threads);
	printf("%d\n", resultado);
	return 0;
}


