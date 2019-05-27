import os

path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/record/'

def create_table(tablename):
	fp = open(path+tablename+'.rec','a')
	fp.close()

def delete_table(tablename):
	os.remove(path+tablename+'.rec')