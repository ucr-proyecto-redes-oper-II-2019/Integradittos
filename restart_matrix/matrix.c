#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include <signal.h>

int sin_interrumpir = 1;

/* ----- Subrutinas y funciones ----------- */
void mult(double X[15][15], double Y[15][15], double Temp[15][15], int dim) {
	int i, j, k;
	for (i=0; i<dim; i++)
	  for (j=0; j<dim; j++) {
		Temp[i][j] = 0;
		for (k=0; k<dim; k++)
		  Temp[i][j] += X[i][k]*Y[k][j];
	  }
	for (i=0; i<dim; i++)
	  for (j=0; j<dim; j++) {
        X[i][j] = Temp[i][j];
	}	  
}
/* -----------------*/

void lea(FILE *fd, double X[15][15], int dim) {
	int i, j;
	for (i=0; i<dim; i++) {
	  for (j=0; j<dim; j++) 
         fscanf(fd, "%lf", &X[i][j]);
	 }
}
/* -----------------*/

void imprima(double X[15][15], int dim) {
	int i, j;
	for (i=0; i<dim; i++) {
	  for (j=0; j<dim; j++) 
         printf("%12.2lf", X[i][j]);
      printf("\n");
	 }
}
/* -----------------*/

void ident(double X[15][15], int dim) {
	int i, j;
	for (i=0; i<dim; i++) {
	  for (j=0; j<dim; j++) 
        if (i == j) X[i][i] = 1.0;
        else X[i][j] = 0.0;
	 }
}
/* -----------------*/

void scalar(double X[15][15], int dim, double val) {
	int i, j;
	for (i=0; i<dim; i++) {
	  for (j=0; j<dim; j++) 
        X[i][j] *= val;
	 }
}
/* -----------------*/

int verify(double X[15][15], int dim) {
	int i, j;
	for (i=0; i<dim; i++) {
	  for (j=0; j<dim; j++) 
        if (i == j) {
			if (X[i][i] != 1.0)
			   return(0);
		}
		else {
		  if (X[i][j] != 0.0)
		     return(0);
		 }
	 }
	 return(1);
}
/* -----------------*/

// Función que atrapa la senal SIGINT
void catcher(int signal)
{
    // Evita que el ciclo en main continúe ejecutándose
    sin_interrumpir = 0;
    exit(0); 
}


/* --------------------------MAIN---------------------------------*/
int main(void) {
/* ----- Variables -----*/
  FILE *fdata, *fout, *fexec;
  int dim, n, i, j, iters, totalprod;
  double A[15][15], B[15][15], I[15][15], Temp[15][15], det, sdet, c;

/* --- Instrucciones ---*/
  // se asigna la subrutina catcher() a la interrupción
  signal(SIGINT, &catcher);

  fdata = fopen("matrices.dat", "r");
  if( fdata == NULL ) {
      perror("Error opening matrices.dat: ");
      return(-1);
   }


   // Intenta abrir el archivo de ejecución para leer (en binario)
    fexec = fopen("execution", "rb");

    // Si el archivo SÍ existía...
    if (fexec != NULL)
    {
    	// lee los datos de ejecución ya guardados
        fread(&iters, sizeof(int), 1, fexec);
        fread(&totalprod, sizeof(int), 1, fexec);
        fclose(fexec);
    }

  fout  = fopen("trace.txt", "w");
  if( fout == NULL ) {
      perror("Error opening trace.txt: ");
      return(-1);
   }
  fclose(fout);

  fscanf(fdata, "%d %lf", &dim, &det);  
  lea(fdata, A, dim);
  lea(fdata, B, dim);
  fclose(fdata);

  sdet = sqrt(det);
  c = 1.0/sdet;
  srand(time(0));
  printf("Leidos: dim=%d, det=%lf, sdet=%lf\n", dim, det, sdet);
  printf("\nMatriz A leida:\n");
  imprima(A, dim);

  printf("\nMatriz B leida:\n");
  imprima(B, dim);
  
  ident(I, dim);
  fexec = fopen("execution", "wb");
  //iters = 0;
  //totalprod = 0;
  while (1) {
	
	int indice = 0; 
  	if( fexec == NULL ) {
      	perror("Error opening execution file: ");
      		return(-1);
   	}
   // guarda los datos de ejecución
   	fwrite(&iters, sizeof(int), 1, fexec);
   	fwrite(&totalprod, sizeof(int), 1, fexec);
	    printf("Iteracion actual %d\n", iters+1);
	fout  = fopen("trace.txt", "a");
    if( fout == NULL ) {
       perror("Error opening trace.txt: ");
       return(-1);
    }
    n = rand() % 6 + 1; 
	primeraParte: 
		for (i = indice; i<n; i++) {
		   mult(I, A, Temp, dim);
		   printf("Mult  \n"); 
		   imprima(I); 
		   scalar(I, dim, c);
		   imprima(I);
		   indice = i; 
		}
	indice = 0; 	
	segundaParte: 
		for (i = indice; i<n; i++) {
		   mult(I, B, Temp, dim);
		   scalar(I, dim, c);
		}
	terceraParte: 
		if (verify(I, dim)) {
			iters++;
			totalprod += 2*n;
			fprintf(fout, "Iteracion %d verificada OK: productos = %d, \ttotalprod = %d\n",
					iters, 2*n, totalprod);
			printf("Completadas %d iteraciones\n", iters);
		}
		else {
			printf("Iter %d presenta error. Se cancela el programa\n", iters+1);
			fprintf(fout, "Iter %d presenta error. Se cancela el programa\n", iters+1);
			exit(1);
		}
		fclose(fout);
		usleep(100000);
  }

  // Abre el archivo de ejecución en modo (sobre)escritura en binario.
  fexec = fopen("execution", "wb");
  if( fexec == NULL ) {
      perror("Error opening execution file: ");
      return(-1);
   }
   // guarda los datos de ejecución
   fwrite(&iters, sizeof(int), 1, fexec);
   fwrite(&totalprod, sizeof(int), 1, fexec);
   fclose(fexec);

  
  return(0);
}
