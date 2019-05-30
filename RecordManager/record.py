import os
import re
import BufferManager.buffer

path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/record/'

def init():
	BufferManager.buffer.init()

def finalize():
	BufferManager.buffer.finalize()

def create_table(tablename):
	BufferManager.buffer.create_table(tablename)

def delete_table(tablename):
	BufferManager.buffer.delete_table(tablename)
	os.remove(path+tablename+'.rec')

def insert(tablename,values):
	encode = '1'
	for value in values:
		if type(eval(value))==str:
			encode+= '{:\0<255}'.format(str(value[1:-1]))
		else:
			encode+= '{:\0<255}'.format(str(value))
	return BufferManager.buffer.save_block(tablename, encode)

def decrypt(code):
	valid_bit= int(code[0])
	attributes = re.split('\0+',code[1:].strip('\0'))
	return valid_bit, attributes

def truncate(tablename, where):
	BufferManager.buffer.truncate(tablename, where)

def print_record(tablename, columnname, clauses, res, length):
	ans = []
	if res == None:
		loc = 0
		while 1:
			code = BufferManager.buffer.get_block(tablename, loc, length).decode('utf-8')
			loc += length
			if code =='':
				break
			vb, entry = decrypt(code)
			if vb:
				flag = True
				for clause in clauses:
					if clause[3]=='char':
						if not eval('entry[clause[-1]]'+clause[1]+clause[2]):
							flag = False
					else:
						if not eval(str(eval('entry[clause[-1]]'))+clause[1]+clause[2]):
							flag = False
				if flag:
					ans.append(entry)
	else:	
		for loc in res:
			code = BufferManager.buffer.get_block(tablename, loc, length).decode('utf-8')
			vb, entry = decrypt(code)
			if vb:
				flag = True
				for clause in clauses:
					if clause[3]=='char':
						if not eval('entry[clause[-1]]'+clause[1]+clause[2]):
							flag = False
					else:
						if not eval(str(eval('entry[clause[-1]]'))+clause[1]+clause[2]):
							flag = False
				if flag:
					ans.append(entry)
	print('+',end='')
	print(('-'*16+'+')*len(columnname))
	for i in columnname:
		if len(str(i)) > 14:
			output = str(i)[0:14]
		else:
			output = str(i)
		print('|',output.center(15),end='')
	print('|')
	print('+',end='')
	print(('-'*16+'+')*len(columnname))
	for i in ans:
		for j in range(len(columnname)):
			if len(str(i[j])) > 14:
				output = str(i[j])[0:14]
			else:
				output = str(i[j])
			print('|',output.center(15) ,end='')
		print('|')
	print('+',end='')
	print(('-'*16+'+')*len(columnname))

def delete_record(tablename, clauses,length):
	loc = 0
	res = []
	while 1:
		code = BufferManager.buffer.get_block(tablename, loc,length).decode('utf-8')
		if code =='':
			break
		vb, entry = decrypt(code)
		if vb:
			flag = True
			for clause in clauses:
				if clause[3]=='char':
					if not eval('entry[clause[-1]]'+clause[1]+clause[2]):
						flag = False
				else:
					if not eval(str(eval('entry[clause[-1]]'))+clause[1]+clause[2]):
						flag = False
			if flag:
				BufferManager.buffer.change_valid_bit(tablename, loc)
				res.append(entry)
		loc += length
	return res

def create_index(tablename, id, type,length):
	loc = 0
	res = []
	while 1:
		code = BufferManager.buffer.get_block(tablename, loc, length).decode('utf-8')
		if code =='':
			break
		vb, entry = decrypt(code)
		if vb:
			if type=='char':
				res.append((loc,entry[id]))
			else:
				res.append((loc,eval(entry[id])))
		loc += length
	return res
			
