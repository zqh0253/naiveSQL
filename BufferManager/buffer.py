import os

cache = []
path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/record/'
fp = {}

def init():
	file_list = os.listdir(path)
	for file in file_list:
		print(file)
		fp[file.rstrip('.rec')] = open(path+file,'a+')

def finalize():
	file_list = os.listdir(path)
	for file in file_list:
		fp[file.rstrip('.rec')].close()
# def load_block(n):

def save_block(tablename, encode):
	if tablename not in fp:
		fp[tablename] = open(path+tablename+'.rec','a+')
	fp[tablename].write(encode)		
	return(fp[tablename].tell())

# def get_unsaved_number_in_lru():
