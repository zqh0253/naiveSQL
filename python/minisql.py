import cmd
import time
import os
import sys

import APIManager.api

class miniSQL(cmd.Cmd):
	intro = 'Welcome to the MiniSQL database server.\nType help or ? to list commands.\n'
	
	def emptyline(self):
		pass

	def default(self, line):
		args, symbol = line, line.split()[0] 
		if (symbol not in ['select','create','drop','insert','delete','quit','execfile']):
			print('Unrecognized command.')
			return
		while (args.find(';')==-1):
			print('.......>',end='')
			args += (' '+input())
		try:
			eval('APIManager.api.'+symbol)(args.replace(';',''))
		except Exception as e:
			print(str(e))


if __name__ == '__main__':
	
	# miniSQL.prompt = '(%s)' % sys.argv[2] + 'MiniSQL > '
	miniSQL.prompt = 'MiniSQL>' 
	miniSQL().cmdloop()

