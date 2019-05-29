import sys
import minisql
import CatalogManager.catalog
import IndexManager.index
import RecordManager.record

def init():
	RecordManager.record.init()
	IndexManager.index.init()
	CatalogManager.catalog.init()

def finalize():
	RecordManager.record.finalize()
	IndexManager.index.finalize()
	CatalogManager.catalog.finalize()

def create(words):
	if words[1] == 'table':
		tablename,attributes,cnt,length,primary = words[2],[],3,len(words),None
		while (1):
			unique = 0
			if cnt + 1 < length and words[cnt]=='primary':
				if cnt+2==length:
					raise Exception("Syntax error, primary key [attribute] expected.")
				if words[cnt+1]!='key':
					raise Exception("key expected, but "+words[cnt+1]+' found')
				primary = words[cnt+2]
				cnt += 3
			else:
				if cnt + 1== length:
					raise Exception('type of '+words[cnt]+' expected.')
				if words[cnt + 1] not in ['char','int','float']:
					raise Exception('type '+words[cnt+1]+' unsupported.')
				if words[cnt+1] in ['int','float']:
					if (cnt + 2 < length) and (words[cnt+2]=='unique'):
						unique = 1
					attributes.append([words[cnt], words[cnt+1], 0,[], unique])
					cnt += (2+unique)
				else:
					if cnt + 2 == length:
						raise Exception("maximum length of char expected.")
					if cnt + 3 < length and words[cnt+3]=='unique':
						unique = 1
					attributes.append([words[cnt], words[cnt+1], int(words[cnt+2]), [], unique])
					cnt += (3+unique)
			if cnt  == length:
				print(attributes,primary,tablename)
				CatalogManager.catalog.exist_table(tablename, True)
				CatalogManager.catalog.create_table(tablename,attributes,primary)
				IndexManager.index.create_table(tablename,' ')
				RecordManager.record.create_table(tablename)
				break
	elif words[1] == 'index':
		if len(words)!=6 or words[3]!='on':
			raise Exception("Syntax error. Type \'help create\' for instructions.")
		print(words[2],words[4],words[5])
	else:
		raise Exception('[table/index] expected, but '+words[1]+' found.')

def drop(words):
	if words[1]=='table':
		print(words[2])
		CatalogManager.catalog.exist_table(words[2], False)
		IndexManager.index.delete_table(words[2])
		CatalogManager.catalog.delete_table(words[2])
		RecordManager.record.delete_table(words[2])
	elif words[1]=='index':
		tablename=IndexManager.index.delete_index(words[2])
		CatalogManager.catalog.delete_index(tablename,words[2])
	else:
		raise Exception('[table/index] expected, but '+words[1]+' found.')

def insert(words):
	if len(words)<5:
		raise Exception('Syntax error. Type \'help insert\' for instructions.')
	if words[1]!='into':
		raise Exception('into expected, but '+words[1]+' found.')
	if words[3]!='values':
		raise Exception('values expected, but '+words[3]+' found.')
	CatalogManager.catalog.exist_table(words[2],False)
	CatalogManager.catalog.check_type(words[2],words[4:])
	where = RecordManager.record.insert(words[2],words[4:])
	print(words[4:])
	for index,key in enumerate(words[4:]):
		if CatalogManager.catalog.get_index_name(words[2], index) != []:
			for indexname in CatalogManager.catalog.get_index_name(words[2], index):
				IndexManager.index.insert_entry(words[2],indexname,eval(key),where)

def select(words):
	if len(words)<6:
		raise Exception('Syntax error. Type \'help select\' for instructions.')
	if words[1]!='*':
		raise Exception('* expected, but '+words[1]+' found.')
	if words[2]!='from':
		raise Exception('from expected, but '+words[2])+' found.'
	if len(words)==4:
		print("NULL")
	else:
		if words[4]!='where':
			raise Exception('where expected, but '+words[4]+' found')

		cnt,clauses = 5,[]
		while (1):
			if cnt+3>len(words):
				raise Exception('Clause is not complete.')
			if words[cnt+1] not in ['<','<=','>','>=','=','<>']:
				raise Exception('Input operator '+words[cnt+1]+' is not supported.')
			clauses.append([words[cnt],words[cnt+1],words[cnt+2]])
			if cnt+3==len(words):
				print(clauses)
				break
			if words[cnt+3] !='and':
				raise Exception('and expected but '+words[cnt+3]+' found.')
			cnt += 4

def delete(words):
	if len(words)<3:
		raise Exception('Syntax error. Type \'help delete\' for instructions.')
	if words[1]!='from':
		raise Exception('from expected, but '+words[1]+' found.')
	if len(words)==3:
		print(words[2])
	else:
		if words[3]!='where':
			raise Exception('where expected, but '+words[3]+' found')

		cnt,clauses = 4,[]
		while (1):
			if cnt+3>len(words):
				raise Exception('Clause is not complete.')
			if words[cnt+1] not in ['<','<=','>','>=','=','<>']:
				raise Exception('Input operator '+words[cnt+1]+' is not supported.')
			clauses.append([words[cnt],words[cnt+1],words[cnt+2]])
			if cnt+3==len(words):
				print(clauses)
				break
			if words[cnt+3] !='and':
				raise Exception('and expected but '+words[cnt+3]+' found.')
			cnt += 4	