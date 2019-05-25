#include<iostream>

#include "Interpreter.h"
#include "Head.h"

using namespace std;

Interpreter::Interpreter(){
	is_end = 0;
	is_quit = 0;
	has_valid_input = 0;
	has_primary = 0;
}

void Interpreter::refresh(){
	is_end = 0;
	has_valid_input = 0;
	has_primary = 0;
	tokens.clear();
	attributes.clear();
}

void Interpreter::split(string sql){
// split the string sql into vector<string> tokens
	for(int i=0;i<sql.size();i++){
		if (sql[i]==';'){
			is_end = 1;
			return;
		}
		if (!(sql[i]==' ' || sql[i]=='(' || sql[i]==')' || sql[i]==',')){
			int start_loc = i;
			while(!(sql[i]==' ' || sql[i]=='(' || sql[i]==')' || sql[i]==',' || sql[i]==';'))
				i++;
			i--;
			tokens.push_back(sql.substr(start_loc,i-start_loc+1));
			has_valid_input = 1;
		}
	}
}

void Interpreter::raise_unexpected(string loc, string expected_content, string found_content){
	cerr << loc << " expecting " << expected_content << " but found " << found_content << endl;
}

void Interpreter::execute(string sql){
	split(sql);

	if (is_end){
		try{
			if (tokens.size()<3) 
				throw "Too short";
			if (tokens[0]=="create"){
				if (tokens[tokens.size()-3] != "primary") throw "Primary key needed!";
				if (tokens[tokens.size()-2] != "key") throw "Syntax error! key expected.";
				for (auto x:tokens){cout<<x<<" ";}cout<<endl;
				if(tokens[1]=="table"){
					for (int i = 3;;){
						if(tokens.size()<i+2)
							throw "Too short1";
						if(tokens[i+1]!="int"&&tokens[i+1]!="float"&&tokens[i+1]!="char")
							throw "fucking type1";
						if(tokens[i+1]=="int"||tokens[i+1]=="float"){
							attributes.push_back(Form(tokens[i],
													  tokens[i+1]=="int"?INT_TYPE:FLOAT_TYPE,
													  0,(tokens.size()>i+2 && tokens[i+2]=="unique"),0));
							i+=(2+(tokens.size()>i+2 && tokens[i+2]=="unique"));
						}
						else if(tokens[i+1]=="char"){
							if(tokens.size()<i+3)
								throw "Too short2";
							attributes.push_back(Form(tokens[i],
													  CHAR_TYPE,
													  atoi(tokens[i+2].c_str()),(tokens.size()>i+3 && tokens[i+3]=="unique"),0));
							i+=(3+(tokens.size()>i+3 && tokens[i+3]=="unique"));
						}
						if (i==tokens.size()-3) break;
					}
					int flag = 1;
					for (auto &x : attributes){
						if (x.name==tokens[tokens.size()-1]){
							x.primary = 1;
							flag = 0;
						}
					}
					if (flag) throw "No primary key founded!";
					
					//api->create_table
					for (auto x :attributes){
						x.ptr();
					}

				}
				else if (tokens[1]=="index"){

				}
				else{
					raise_unexpected("created object's type","[table, index]",tokens[1]);
				}
			}	
			else if (tokens[0]=="drop"){
				if(tokens[1]!="table" && tokens[1]!="index") throw "[table, index] expected";
				if(tokens[1]=="table"){
					//api->drop_table
					cout << "drop_table" << tokens[2];
				}else{
					//api->drop_index
					cout <<"drop_index" << tokens[2];
				}
			}
			else if (tokens[0]=="select"){

			}
			else if (tokens[0]=="insert"){

			}
			else if (tokens[0]=="delete"){

			} 
			else if (tokens[0]=="quit"){
				is_quit = 1;
			}
			else if (tokens[0]=="execfile"){

			}
			else {
				raise_unexpected("Function name","[create, drop, select, insert, delete, quit, execfile]",tokens[0]);
			}
		}
		catch(const char* msg){
			cerr << msg;
		}
	}
}