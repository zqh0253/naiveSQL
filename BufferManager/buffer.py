import os
import re
import collections

cache = collections.OrderedDict()
cache_size = 1000
path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/record/'
fp = {}

def init():
	pass
def finalize():
	namelist=[]
	for name, code in cache.items():
		tablename, where = re.split('\0',name)
		if tablename not in namelist:
			namelist.append(tablename)
			with open(path+tablename+'.rec','a+') as fp:
				pass
		with open(path+tablename+'.rec','rb+') as fp:
			fp.seek(int(where))
			fp.write(code)

def save_block(tablename, code):
	with open(path+tablename+'.rec','rb+') as fp:
		fp.read()
		if len(cache)==cache_size:
			cache.popitem(last=False)
		cache[tablename+'\0'+str(fp.tell())] = code.encode(encoding='UTF-8',errors='strict')
		fp.write(cache[tablename+'\0'+str(fp.tell())])
		return(fp.tell())

def get_block(tablename, where, length):
	if tablename+'\0'+str(where) in cache:
		return cache[tablename+'\0'+str(where)]
	with open(path+tablename+'.rec','rb+') as fp:
		fp.seek(where)
		if len(cache)==cache_size:
			cache.popitem(last=False)
		cache[tablename+'\0'+str(where)] = fp.read(length)
	return cache[tablename+'\0'+str(where)]

def create_table(tablename):
	p = open(path+tablename+'.rec','a+')
	p.close()

def delete_table(tablename):
	pass

def truncate(tablename, where):
	fp[tablename].seek(where)
	fp[tablename].truncate()

def change_valid_bit(tablename, loc):
	with open(path+tablename+'.rec','rb+') as fp:
		if tablename+'\0'+str(loc) not in cache:
			cache.popitem(last=False)
		l = list(cache[tablename+'\0'+str(loc)].decode('utf-8'))
		l[0] = '0'
		cache[tablename+'\0'+str(loc)] = ''.join(l).encode(encoding='UTF-8',errors='strict')
		fp.seek(loc)
		fp.write('0'.encode(encoding='UTF-8',errors='strict'))
