#include <future>
#include <iostream>
#include <cstdlib>
#include "int_adder.h"
#include "lower_layer.h"


int IntAdder::run(int size, char * array [])
{
	if (size < 1)
	{
		// No params
		std::cout << "\nNo elements in the array.\n\n";
		return -1;
	}

	std::cout << std::endl;

	int * intArr = new int [size];
	for (int elem = 0; elem < size; ++elem)
	{
		intArr[elem] = atoi(array[elem]);
		std::cout << intArr[elem];
		if (elem != size-1) std::cout << " + ";
	}
	std::cout << " = ";

	int threadAmnt = std::thread::hardware_concurrency();
	std::future<int> * results = new std::future<int>[threadAmnt];

	int elementsPerThread = size / threadAmnt;
	int threadsWithExtraElem = size % threadAmnt;

	int start = 0;

	for (int th = 0; th < threadAmnt; ++th)
	{
		if (th < threadsWithExtraElem)
		{
			results[th] = std::async(std::launch::async, &IntAdder::rangeSum, elementsPerThread+1, intArr+start);
			start += (elementsPerThread+1);
		}
		else
		{
			results[th] = std::async(std::launch::async, &IntAdder::rangeSum, elementsPerThread, intArr+start);
			start += (elementsPerThread);
		}
	}

	int totalSum = 0;

	for (int th = 0; th < threadAmnt; ++th)
	{
		totalSum = LowerLayer::add(totalSum, results[th].get());
	}

	std::cout << totalSum << "\n\n";

	delete intArr;
	return 0;
}

int IntAdder::rangeSum(int size, int * array)
{
	int sum = 0;
	for (int index = 0; index < size; ++index)
	{
		sum = LowerLayer::add(sum, array[index]);
	}
	return sum;
}