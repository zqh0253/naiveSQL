#include <iostream>
#include "Minisql.h"
#include "Interpreter.h"
using namespace std;

void Minisql::init(){
	cout <<"Fake initing..";
}

int main(){
	Minisql::init();
	Interpreter* interpreter = new Interpreter();

	string sql;
	while (!interpreter->is_quit){
		while(!interpreter->is_end){
			if(!interpreter->has_valid_input)
				cout << endl << "Minisql >";
			else 
				cout << "...>";
			getline(cin, sql);
			interpreter->execute(sql);	
		}
		interpreter->refresh();
	}

	// Minisql::delete();
	return 0;
}