import os
import BufferManager.buffer

path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/record/'

def init():
	BufferManager.buffer.init()

def finalize():
	BufferManager.buffer.finalize()

def create_table(tablename):
	fp = open(path+tablename+'.rec','a')
	fp.close()

def delete_table(tablename):
	os.remove(path+tablename+'.rec')

def insert(tablename,values):
	encode = '1'
	for value in values:
		if type(eval(value))==str:
			encode+= '{:_<50}'.format(str(value[1:-1]))
		else:
			encode+= '{:_<50}'.format(str(value))
	print(encode)
	return BufferManager.buffer.save_block(tablename, encode)
