import json
import os

path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/catalog/'
def exist_table(tablename, boolean):
	fp = open(path+'table.sqlf')
	tablelist = json.loads(fp.read())
	fp.close()
	if (tablename in tablelist) if boolean else (tablename not in tablelist):
		raise Exception('Table '+tablename+' already exists.') if boolean else Exception('Table '+tablename+' does not exist.')

def create_table(tablename, attributes,primary):
	if primary==None:
		raise Exception('primary key must be specified.')
	fp = open(path+'table.sqlf','a+')
	fp.seek(0)
	tablelist = json.loads(fp.read())
	m = {"primary":[x[0] for x in attributes].index(primary),"columns":{}}
	for x in attributes:
		m["columns"][x[0]]=x[1:]
	m['columns'][primary][-1] = 1
	m['columns'][primary][-2].append(' ')
	tablelist[tablename]=m
	fp.seek(0)
	fp.truncate()
	fp.write(json.dumps(tablelist))
	fp.close()

def delete_table(tablename):
	fp = open(path+'table.sqlf','a+')
	fp.seek(0)
	tablelist = json.loads(fp.read())
	tablelist.pop(tablename)
	fp.seek(0)
	fp.truncate()
	fp.write(json.dumps(tablelist))
	fp.close()

def get_index_list(tablename):
	fp = open(path+'table.sqlf','a+')
	fp.seek(0)
	tablelist = json.loads(fp.read())
	l=[]
	return [y for y in [x[-2] for x in tablelist[tablename]['columns'].items()]]

def delete_index(tablename,indexname):
	fp = open(path+'table.sqlf','a+')
	fp.seek(0)
	tablelist = json.loads(fp.read())
	for attr in tablelist[tablename]['columns'].keys():
		if (indexname,cnt) in zip(tablelist[tablename]['columns'][attr][-2],range(len(tablelist[tablename]['columns'][attr][-2]))):
			tablelist[tablename]['columns'][attr][-2].pop(cnt)
			break