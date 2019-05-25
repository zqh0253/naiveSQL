res.exe : Minisql.cpp Interpreter.cpp  Head.cpp
	g++ Head.cpp Minisql.cpp Interpreter.cpp  -o res -std=c++11
