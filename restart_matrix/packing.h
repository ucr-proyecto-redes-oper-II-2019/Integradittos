#ifndef PACKING
#define PACKING

#include <stdio.h>

int pack_process(long file_count, char * file_names[], FILE * archivo_proceso);
int unpack_process(FILE * archivo_proceso);

#endif //PACKING