#ifndef _INTERPRETER_H
#define _INTERPRETER_H

#include <vector>
#include <string>

using namespace std;

class Interpreter{
	public:
		int is_end;
		int is_quit;
		int has_valid_input;


		Interpreter();
		void execute (string sql);
		void refresh();
	private:
		vector<string> tokens;
		vector<string> names;
		vector<int> types;
		vector<int> sizes;
		int ptr;
		void split(string sql);
		void raise_unexpected(string loc, string expected_content, string found_content);
};

#endif