import cmd
import time
import os
import sys
import re

import ApiManager.api

class miniSQL(cmd.Cmd):
	intro = 'Welcome to the MiniSQL database server.\nType help or ? to list commands.\n'
	
	def finalize(self):
		print('oh,')

	def emptyline(self):
		pass

	def default(self, line):
		args, symbol = line, line.split()[0]
		if (symbol[:4]=="quit"):
			self.finalize()
			print('goodbye')
			sys.exit() 
		if (symbol not in ['select','create','drop','insert','delete','quit','execfile']):
			print('Unrecognized command.')
			return
		while (args.find(';')==-1):
			print('.......>',end='')
			args += (' '+input())
		try:
			args = args.replace('<',' < ').replace('>',' > ').replace('=',' = ').replace('>=',' >= ').replace('<=',' <= ').replace('<>',' <> ')
			args = re.sub(r' +', ' ', args.replace(';','')).strip().replace('\u200b','')
			words = [word for word in re.split(' |\(|\)|,',args) if word!='']
			eval('ApiManager.api.'+symbol)(words)
		except Exception as e:
			print(str(e))


if __name__ == '__main__':
	
	# miniSQL.prompt = '(%s)' % sys.argv[2] + 'MiniSQL > '
	miniSQL.prompt = 'MiniSQL>' 
	miniSQL().cmdloop()

