import os
import CatalogManager.catalog

path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/index/'

def create_table(tablename,indexname):
	fp = open(path+tablename+'_'+indexname+'.ind','a')
	fp.close()

def delete_table(tablename):
	list = CatalogManager.catalog.get_index_list(tablename)
	for indexname in list:
		os.remove(path+tablename+'_'+indexname+'.ind')

def delete_index(indexname):
	file_list = os.listdir(path)
	for file in file_list:
		if indexname == file.split('_')[1]:
			os.remove(path+file)
			return file.split('_')[0]
	# raise Exception('No index named '+indexname+'.')
