import os

cache = []
path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/record/'
fp = {}

def init():
	global fp
	file_list = os.listdir(path)
	for file in file_list:
		print(file)
		fp[file.rstrip('.rec')] = open(path+file,'a+')

def finalize():
	global fp
	for f in fp.values():
		f.close()
# def load_block(n):

def save_block(tablename, encode):
	global fp
	if tablename not in fp:
		fp[tablename] = open(path+tablename+'.rec','a+')
	fp[tablename].write(encode)		
	return(fp[tablename].tell())

def create_table(tablename):
	p = open(path+tablename+'.rec','a+')
	fp[tablename] = p

def delete_table(tablename):
	global fp
	fp[tablename].close()

def truncate(tablename, where):
	fp[tablename].seek(where)
	fp[tablename].truncate()

# def get_unsaved_number_in_lru():
