#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>
#include "suma.h"

int sumar_vector(int * vector, int countThreads)
{
	int resultados[countThreads]; 
	int temporal[countThreads]; 
	int sumas_de_vectores = countThreads / 2;
	int cantidad_sumas = countThreads / 2;

	memcpy(resultados, vector, countThreads * sizeof(int));
	
	
	for(int i = 0; i < sumas_de_vectores; i++)
	{ 	
		#pragma omp parallel for num_threads(cantidad_sumas) shared(resultados)
		for(int j = 0; j < cantidad_sumas; j++)
		{
			printf("hilo %d suma: %d con %d\n", omp_get_thread_num(),resultados[j*2], resultados[j*2+1] );
			temporal[j] = suma(resultados[j*2], resultados[j*2+1]);
		}

		cantidad_sumas /= 2;
		memcpy(resultados, temporal, countThreads * sizeof(int));
	}
	return resultados[0];
}

int main(int argc, char* argv[])
{
 	int threads = atoi(argv[1]);
	int vectorInicial[ ] = {2,3,4,5,6,7,8,9};
	
	int resultado = sumar_vector(vectorInicial,threads);
	printf("%d\n", resultado);
	return 0;
}


