import json
import os

path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/catalog/'
def exist_table(tablename):
	fp = open(path+'table.sqlf')
	tablelist = json.loads(fp.read())
	print(tablelist)
	fp.close()
	if tablename in tablelist.items():
		raise Exception('Table '+tablename+' already exists.')

def create_table(tablename, attributes,primary):
	fp = open(path+'table.sqlf','a+')
	fp.seek(0)
	tablelist = json.loads(fp.read())
	m = {"primary":[x[0] for x in attributes].index(primary),"columns":{}}
	for x in attributes:
		m["columns"][x[0]]=x[1:]
	tablelist[tablename]=m
	fp.seek(0)
	fp.truncate()
	fp.write(json.dumps(tablelist))
	fp.close()

def 