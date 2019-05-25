#include <iostream>

#include "Head.h"

Form::Form(string _name, int _type, int _size, int _unique, int _primary):name(_name),type(_type),size(_size),
																		unique(_unique),primary(_primary){}

void Form::ptr(){
	cout << name << " " << type << " " << size << " " << unique << " " << primary <<endl;
}
