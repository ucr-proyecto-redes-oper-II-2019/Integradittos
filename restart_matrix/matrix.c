#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include <signal.h>
#define TAMANOMATRIX 1800
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
void guardar(FILE * fexec, double matrix[15][15], int iters, int totalprod, int numero_de_etiqueta, int indice, int n)
{
	// lee los datos de ejecución ya guardados
	fwrite(&iters, sizeof(int), 1, fexec);
	fwrite(&totalprod, sizeof(int), 1, fexec);
	//fwrite(&matrix, sizeof(double), 15*15, fexec);
	fwrite(&indice, sizeof(int), 1, fexec);
	fwrite(&n, sizeof(int), 1, fexec);
	imprima(matrix, 15);
	//fclose(fexec);
}
/* -----------------*/
// Función que atrapa la senal SIGINT
void catcher(int signal)
{
    // Evita que el ciclo en main continúe ejecutándose
    sin_interrumpir = 0;
}

/* --------------------------MAIN---------------------------------*/
int main(void) {
/* ----- Variables -----*/
	int indice = 0; 
	FILE *fdata, *fout, *fexec;
	int dim, n, i, j, iters, totalprod;
	double A[15][15], B[15][15], I[15][15], Temp[15][15], det, sdet, c;
	int bandera = 1; 
	int numero_de_etiqueta = 0; 
/* --- Instrucciones ---*/
  // se asigna la subrutina catcher() a la interrupción
	signal(SIGINT, &catcher);
	fdata = fopen("matrices.dat", "r");
	if( fdata == NULL ) 
	{
		perror("Error opening matrices.dat: ");
		return(-1);
	}
   // Intenta abrir el archivo de ejecución para leer (en binario)
    fexec = fopen("execution", "rb");
	//------------------------------------------Se carga el archivo ----------------------------------------
    // Si el archivo SÍ existía...
    if (fexec != NULL)
    {
		// lee los datos de ejecución ya guardados
        fread(&iters, sizeof(int), 1, fexec);
        fread(&totalprod, sizeof(int), 1, fexec);
		//fread(&I, sizeof(double),15*15 , fexec);
		fread(&numero_de_etiqueta, sizeof(int), 1, fexec);
		fread(&indice, sizeof(int), 1, fexec);
		fread(&n, sizeof(int), 1, fexec);
		
		printf("Este es el numero de iteracin guardado. %d \n", iters);
        fclose(fexec);
		fout  = fopen("trace.txt", "w");
		if( fout == NULL ) 
		{
			perror("Error opening trace.txt: ");
			return(-1);
		}
		imprima(I, 15);
		
		fclose(fout);
		fscanf(fdata, "%d %lf", &dim, &det);  
		lea(fdata, A, dim);
		lea(fdata, B, dim);
		fclose(fdata);
		sdet = sqrt(det);
		c = 1.0/sdet;
		printf("Hola este es el valor de c %f \n", c);
		srand(time(0));	  
		fexec = fopen("execution", "wb");
		if(numero_de_etiqueta = 1)
		{
			goto primeraParte; 
		}
		if(numero_de_etiqueta = 2)
		{
			goto segundaParte;
		}
		if(numero_de_etiqueta)
		{
			goto terceraParte;
		}
		goto partePrincipal;
    }
    //------------------------------------------------se termina de cargar el archivo -----------------------------------------------------
  fout  = fopen("trace.txt", "w");
  if( fout == NULL ) 
  {
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
  printf("Hola este es el valor de c2 %f \n", c);
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
  partePrincipal:
   ident(I, dim);
  while (1) 
  {
	
  	if( fexec == NULL)
  	{
      	perror("Error opening execution file: ");
      	return(-1);
   	}
   // guarda los datos de ejecución
   	//fwrite(&iters, sizeof(int), 1, fexec);
   	//fwrite(&totalprod, sizeof(int), 1, fexec);
	printf("Iteracion actual %d\n", iters+1);
	fout  = fopen("trace.txt", "a");
    if( fout == NULL )
     {
       perror("Error opening trace.txt: ");
       return(-1);
    }
    n = rand() % 6 + 1; 
	indice = 0; 
	primeraParte:
		numero_de_etiqueta = 1; 
		for (i = indice; i<n; i++) 
		{
		   mult(I, A, Temp, dim);
		   scalar(I, dim, c);
		   indice = i;
		   if(sin_interrumpir == 0)
		   {
				guardar(fexec, I, iters, totalprod, numero_de_etiqueta, indice+1, n);
				goto fin; 
		   }
		}
	indice = 0; 	
	segundaParte:
		numero_de_etiqueta = 2; 
		for (i = indice; i<n; i++) 
		{
		   mult(I, B, Temp, dim);
		   scalar(I, dim, c);
		   indice = i;
		   if(sin_interrumpir == 0)
		   {
				guardar(fexec, I, iters, totalprod, numero_de_etiqueta, indice+1, n);
				goto fin; 
		   }
		}
	terceraParte:
		numero_de_etiqueta = 3; 
		if (verify(I, dim)) 
		{
			iters++;
			totalprod += 2*n;
			fprintf(fout, "Iteracion %d verificada OK: productos = %d, \ttotalprod = %d\n",
					iters, 2*n, totalprod);
			printf("Completadas %d iteraciones\n", iters);
		}
		else 
		{
			//imprima(I, 15); 
			printf("Iter %d presenta error. Se cancela el programa\n", iters+1);
			fprintf(fout, "Iter %d presenta error. Se cancela el programa\n", iters+1);
			exit(1);
		}
		fclose(fout);
		usleep(100000);
  }

		// Abre el archivo de ejecución en modo (sobre)escritura en binario. 
	   // guarda los datos de ejecución
	   guardar(fexec,I, iters, totalprod, numero_de_etiqueta, 0, n);
	   fin: 
	   fclose(fexec);
  return(0);
}
