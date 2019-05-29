import json
import os

path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/catalog/'

def init():
	print('catalog init')

def finalize():
	print('catalog finalize')

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
	[[l.append(y) for y in x[-2]] for x in tablelist[tablename]['columns'].values()]
	return l

def get_index_name(tablename,index):
	fp = open(path+'table.sqlf','a+')
	fp.seek(0)
	tablelist = json.loads(fp.read())
	return tablelist[tablename]['columns'][list(tablelist[tablename]['columns'].keys())[index]][-2]

def delete_index(tablename,indexname):
	fp = open(path+'table.sqlf','a+')
	fp.seek(0)
	tablelist = json.loads(fp.read())
	for attr in tablelist[tablename]['columns'].keys():
		if (indexname,cnt) in zip(tablelist[tablename]['columns'][attr][-2],range(len(tablelist[tablename]['columns'][attr][-2]))):
			tablelist[tablename]['columns'][attr][-2].pop(cnt)
			break

def check_type(tablename,input_list):
	fp = open(path+'table.sqlf','a+')
	fp.seek(0)
	tablelist = json.loads(fp.read())
	values = []
	for inp,(name,attribute) in zip(input_list,tablelist[tablename]['columns'].items()):
		if attribute[0]=='int':
			value = int(inp)
			values.append(value)
		elif attribute[0]=='float':
			value = float(inp)
			values.append(value)
		else:
			if len(inp)>attribute[1]:
				raise Exception(name + 'has maximum length '+ str(attribute[1]+'.'))
			values.append(inp)
	return values

