import os

cache = []
path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/record/'
fp = {}

def init():
	global fp
	file_list = os.listdir(path)
	for file in file_list:
		fp[file.rstrip('.rec')] = open(path+file,'rb+')

def finalize():
	global fp
	for f in fp.values():
		f.close()
# def load_block(n):

def save_block(tablename, code):
	global fp
	if tablename not in fp:
		fp[tablename] = open(path+tablename+'.rec','rb+')
	fp[tablename].write(code.encode(encoding='UTF-8',errors='strict'))	
	return(fp[tablename].tell())

def get_block(tablename, where, length):
	fp[tablename].seek(where)
	return fp[tablename].read(length)

def create_table(tablename):
	p = open(path+tablename+'.rec','a+')
	p.close()
	p = open(path+tablename+'.rec','rb+')
	fp[tablename] = p

def delete_table(tablename):
	global fp
	fp[tablename].close()

def truncate(tablename, where):
	fp[tablename].seek(where)
	fp[tablename].truncate()

def change_valid_bit(tablename, loc):
	fp[tablename].seek(loc)
	fp[tablename].write('0'.encode(encoding='UTF-8',errors='strict'))