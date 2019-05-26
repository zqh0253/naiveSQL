#include <iostream>

#include "Head.h"

Form::Form(string _name, int _type, int _size, int _unique, int _primary, int _has_index):name(_name),type(_type),size(_size),
																		unique(_unique),primary(_primary),has_index(_has_index){}

void Form::ptr(){
	cout << name << " " << type << " " << size << " " << unique << " " << primary <<endl;
}

Clause::Clause(string _name, int _type, string _value):name(_name),type(_type){int i;for (i=0;i<_value.size();i++) value[i]=_value[i]; value[i]=0;}

const int Clause::LESS_TYPE = 1;  // < .   < 1 = 2 > 4 
const int Clause::LEQ_TYPE = 3;   // <=
const int Clause::GREAT_TYPE = 4; // >
const int Clause::GEQ_TYPE = 6;   // >=
const int Clause::EQUAL_TYPE = 2; // =
const int Clause::NEQ_TYPE = 5;   // <>

void Clause::ptr(){
	int i;
	cout << name<<" "<<type<<" ";
	for (i=0;i<255;i++) {if (value[i] == 0) break; cout <<value[i];}

}

int Clause::type_converter(string op){
	if (op == "<") return 1;
	if (op == "<=") return 3;
	if (op == ">") return 4;
	if (op == ">=") return 6;
	if (op == "=") return 2;
	if (op == "<>") return 5;
}