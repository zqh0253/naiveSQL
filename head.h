#ifndef _HEAD_H
#define _HEAD_H

#include <string>
#include <string.h>

#define INT_TYPE 0
#define FLOAT_TYPE 1
#define CHAR_TYPE 2

using namespace std;

class Form{
public:
	Form(string _name, int _type, int _size, int _unique, int _primary);
	string name;
	int type;
	int size;
	int unique;
	int primary;

	void ptr();
};

#endif