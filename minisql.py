import cmd
import time
import os
import sys
import re
import datetime
import ApiManager.api

def clock(func):
    def int_time(*args, **kwargs):
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        over_time = datetime.datetime.now() 
        total_time = (over_time-start_time).total_seconds()
        print('Run successfully. Passed {} s'.format(total_time))
    return int_time

class miniSQL(cmd.Cmd):
	intro = 'Welcome to the MiniSQL database server.\nType help or ? to list commands.\n'
	
	def finalize(self):
		ApiManager.api.finalize()

	def emptyline(self):
		pass

	@clock
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
			args = args.replace('>=',' >= ').replace('<=',' <= ').replace('<>',' <> ')
			args = re.sub('<(?![=>])',' < ',args)
			args = re.sub('(?<!<)>(?!=)',' > ',args)
			args = re.sub('(?<![<>])=',' = ',args)
			# string(?=pattern) check from left to right
			# (?<=pattern)string check from right to left
			args = re.sub(r' +', ' ', args.replace(';','')).strip().replace('\u200b','')
			words = [word for word in re.split(' |\(|\)|,',args) if word!='']
			eval('ApiManager.api.'+symbol)(words)
		except Exception as e:
			print(str(e))

	def init(self):
		ApiManager.api.init()

if __name__ == '__main__':
	miniSQL().init()
	miniSQL.prompt = 'MiniSQL>' 
	miniSQL().cmdloop()