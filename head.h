#ifndef _HEAD_H
#define _HEAD_H

#include <string>
#include <map>
#include <string.h>

#define INT_TYPE 0
#define FLOAT_TYPE 1
#define CHAR_TYPE 2

using namespace std;

class Form{
	public:
		Form(string _name, int _type, int _size, int _unique, int _primary, int _has_index);
		string name;
		int type;
		int size;
		int unique;
		int primary;
		int has_index;

		void ptr();
};

class Clause{
	public:
		Clause(string _name, int _type, string _value);
		string name;
		int type;
		char value[255];

		void ptr();

		static const int LESS_TYPE;
		static const int LEQ_TYPE;
		static const int GREAT_TYPE;
		static const int GEQ_TYPE;
		static const int EQUAL_TYPE;
		static const int NEQ_TYPE;

		static int type_converter(string op);
};

#endif