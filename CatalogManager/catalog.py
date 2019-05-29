import json
import os

path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/catalog/'

fp = None
tablelist = None

def init():
	global fp, tablelist
	fp = open(path+'table.sqlf','a+')
	fp.seek(0)
	tablelist = json.loads(fp.read())
	print('catalog init')

def finalize():
	fp.seek(0)
	fp.truncate()
	fp.write(json.dumps(tablelist))
	fp.close()
	print('catalog finalize')

def exist_table(tablename, boolean):
	if (tablename in tablelist) if boolean else (tablename not in tablelist):
		raise Exception('Table '+tablename+' already exists.') if boolean else Exception('Table '+tablename+' does not exist.')

def create_table(tablename, attributes,primary):
	if primary==None:
		raise Exception('primary key must be specified.')
	m = {"primary":[x[0] for x in attributes].index(primary),"columns":{}}
	for x in attributes:
		m["columns"][x[0]]=x[1:]
	m['columns'][primary][-1] = 1
	m['columns'][primary][-2].append(' ')
	tablelist[tablename]=m

def delete_table(tablename):
	tablelist.pop(tablename)

def get_index_list(tablename):
	l=[]
	[[l.append(y) for y in x[-2]] for x in tablelist[tablename]['columns'].values()]
	return l

def get_column_with_index(tablename):
	res = []
	for key,value in tablelist[tablename]['columns'].items():
		if value[-1] != []:
			res.append(key)
	return res

def get_index_name(tablename,index):
	return tablelist[tablename]['columns'][index][-2]

def get_index_name_by_seq(tablename,index):
	return tablelist[tablename]['columns'][list(tablelist[tablename]['columns'].keys())[index]][-2]

def delete_index(tablename,indexname):
	for attr in tablelist[tablename]['columns'].keys():
		if (indexname,cnt) in zip(tablelist[tablename]['columns'][attr][-2],range(len(tablelist[tablename]['columns'][attr][-2]))):
			tablelist[tablename]['columns'][attr][-2].pop(cnt)
			break

def get_encode_size(tablename):
	return 255*len(tablelist[tablename]['columns'].keys())+1

def check_type(tablename,input_list):
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