res.exe : Minisql.cpp Interpreter.cpp Head.cpp Api.cpp
	g++ Head.cpp Minisql.cpp Interpreter.cpp Api.cpp -o res -std=c++11
