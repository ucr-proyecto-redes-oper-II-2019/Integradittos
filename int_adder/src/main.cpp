#include "int_adder.h"

int main (int argc, char * argv [])
{
	IntAdder intAdder = IntAdder();
	// Do not include the zeroth parameter
	return intAdder.run(argc-1, argv+1);
}