#include <stdio.h>
#include <omp.h>
#include <string.h>
#include "suma.h"

int main(int argc, char* argv[])
{
 	int threads = argv[0];
	int vectorInicial[ ] = {2,3,4,5,6,7};
	int resultado = sumar_vector(vectorInicial,6);
	printf(resultado);
}

int sumar_vector(int * vector, int countThreads)
{
	int* resultados; 
	int sumas_de_vectores = countThreads / 2;
	int cantidad_sumas = countThreads / 2;
	memcpy(resultados, vector, countThreads);
	
	for(int i = 0; i < sumas_de_vectores; i++)
	{ 
		#pragma omp parrallel for num_threads(countThreads)
		for(int j = 0; j < cantidad_sumas; j++)
		{
			resultados[omp_get_thread_num()] = 
				suma(resultados[omp_get_thread_num()*2], resultados[omp_get_thread_num()*2+1]);

			
		}
		cantidad_sumas /= 2;
	}
	return resultados[0];
}
