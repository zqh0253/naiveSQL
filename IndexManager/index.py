import os
import CatalogManager.catalog

path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/index/'
fp = {}

def init():
	file_list = os.listdir(path)
	for file in file_list:
		fp[file.rstrip('.ind')] = open(path+file,'a+')

def finalize():
	file_list = os.listdir(path)
	for file in file_list:
		fp[file.rstrip('.ind')].close()

def create_table(tablename,indexname):
	p = open(path+tablename+'_'+indexname+'.ind','a')
	fp[tablename] = p

def delete_table(tablename):
	list = CatalogManager.catalog.get_index_list(tablename)
	for indexname in list:
		fp[tablename+'_'+indexname].close()
		os.remove(path+tablename+'_'+indexname+'.ind')

def delete_index(indexname):
	file_list = os.listdir(path)
	for file in file_list:
		if indexname == file.split('_')[1]:
			fp[file.rstrip('.ind')].close()
			os.remove(path+file)
			return file.split('_')[0]
	# raise Exception('No index named '+indexname+'.')

def insert(tablename, key, data):
	
	
