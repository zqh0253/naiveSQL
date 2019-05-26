#ifndef _INTERPRETER_H
#define _INTERPRETER_H

#include <vector>
#include <string>
#include "Head.h"

using namespace std;

class Interpreter{
	public:
		int is_end;
		int is_quit;
		int has_valid_input;
		int has_primary;

		Interpreter();
		void execute (string sql);
		void refresh();
	private:
		vector<string> tokens;
		vector<int> tokens_is_string;
		vector<Form> attributes;
		int ptr;
		void split(string sql);
		void raise_unexpected(string loc, string expected_content, string found_content);
};

#endif