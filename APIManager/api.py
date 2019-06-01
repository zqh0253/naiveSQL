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
				CatalogManager.catalog.exist_table(tablename, True)
				CatalogManager.catalog.create_table(tablename,attributes,primary)
				IndexManager.index.create_table(tablename,' ')
				RecordManager.record.create_table(tablename)
				break
	elif words[1] == 'index':
		if len(words)!=6 or words[3]!='on':
			raise Exception("Syntax error. Type \'help create\' for instructions.")
		indexname,tablename,columnname = words[2], words[4], words[5]
		CatalogManager.catalog.create_index(tablename, indexname, columnname)
		res = RecordManager.record.create_index(tablename,CatalogManager.catalog.get_the_index_of_attribute(tablename,columnname),CatalogManager.catalog.get_type_of_attribute(tablename,columnname) , CatalogManager.catalog.get_encode_size(tablename))
		try:
			IndexManager.index.create_index(tablename, indexname, res)
		except Exception as e:
			raise Exception('Entries sharing same key on the column that is creating index on!')
	else:
		raise Exception('[table/index] expected, but '+words[1]+' found.')

def drop(words):
	if words[1]=='table':
		CatalogManager.catalog.exist_table(words[2], False)
		IndexManager.index.delete_table(words[2],CatalogManager.catalog.get_index_list(tablename))
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
	where = RecordManager.record.insert(words[2],words[4:]) - CatalogManager.catalog.get_encode_size(words[2])
	for index,key in enumerate(words[4:]):
		if CatalogManager.catalog.get_index_name_by_seq(words[2], index) != []:
			for indexname in CatalogManager.catalog.get_index_name_by_seq(words[2], index):
				try:
					IndexManager.index.insert_entry(words[2],indexname,eval(key),where)
				except Exception as e:
					temp_list = CatalogManager.catalog.get_index_name_by_seq(words[2], index)
					for del_indexname in temp_list[:temp_list.index(indexname)]:
						IndexManager.index.delete_entries([e], tablename, del_indexname)
					RecordManager.record.truncate(words[2],where)
					raise Exception('Insertion fails. Data with key: '+str(key)+' already exists.')

def select(words):
	if words[1]!='*':
		raise Exception('* expected, but '+words[1]+' found.')
	if words[2]!='from':
		raise Exception('from expected, but '+words[2])+' found.'
	if len(words)==4:
		RecordManager.record.print_record(words[3],CatalogManager.catalog.get_column_name(words[3]) ,[], None, CatalogManager.catalog.get_encode_size(words[3]))
	else:
		if words[4]!='where':
			raise Exception('where expected, but '+words[4]+' found')

		tablename,cnt,clauses =words[3],5,[]
		while (1):
			if cnt+3>len(words):
				raise Exception('Clause is not complete.')
			if words[cnt+1] not in ['<','<=','>','>=','=','<>']:
				raise Exception('Input operator '+words[cnt+1]+' is not supported.')
			if words[cnt+1]=='<>':
				words[cnt+1] = '!='
			if words[cnt+1]=='=':
				words[cnt+1] = '=='
			clauses.append([words[cnt],words[cnt+1],words[cnt+2],CatalogManager.catalog.get_type_of_attribute(tablename, words[cnt]),CatalogManager.catalog.get_the_index_of_attribute(tablename, words[cnt])] )
			if cnt+3==len(words):
				indexname = CatalogManager.catalog.get_column_with_index(tablename)
				index_clause = None
				for clause in clauses:
					if clause[0] in indexname:
						index_clause = clause
						break
				res = None
				if index_clause != None:
					clauses.remove(clause)
					indexname = CatalogManager.catalog.get_index_name(tablename, index_clause[0])
					res = IndexManager.index.select(tablename,index_clause,indexname[0])
				RecordManager.record.print_record(tablename,CatalogManager.catalog.get_column_name(tablename) ,clauses, res, CatalogManager.catalog.get_encode_size(tablename))
				break
			if words[cnt+3] !='and':
				raise Exception('and expected but '+words[cnt+3]+' found.')
			cnt += 4

def delete(words):
	if len(words)<3:
		raise Exception('Syntax error. Type \'help delete\' for instructions.')
	if words[1]!='from':
		raise Exception('from expected, but '+words[2])+' found.'
	if len(words)==3:
		RecordManager.record.delete_record(words[2], [], CatalogManager.catalog.get_encode_size(words[2]))
		for indexname in CatalogManager.catalog.get_index_list(words[2]):
			IndexManager.index.delete_all(words[2], indexname)
	else:
		if words[3]!='where':
			raise Exception('where expected, but '+words[4]+' found')
		tablename,cnt,clauses =words[2],4,[]
		while (1):
			if cnt+3>len(words):
				raise Exception('Clause is not complete.')
			if words[cnt+1] not in ['<','<=','>','>=','=','<>']:
				raise Exception('Input operator '+words[cnt+1]+' is not supported.')
			if words[cnt+1]=='<>':
				words[cnt+1] = '!='
			if words[cnt+1]=='=':
				words[cnt+1] = '=='
			clauses.append([words[cnt],words[cnt+1],words[cnt+2],CatalogManager.catalog.get_type_of_attribute(tablename, words[cnt]),CatalogManager.catalog.get_the_index_of_attribute(tablename, words[cnt])] )
			if cnt+3==len(words):
				indexname = CatalogManager.catalog.get_column_with_index(tablename)
				res = RecordManager.record.delete_record(tablename,clauses,CatalogManager.catalog.get_encode_size(tablename))
				for cnt,i in enumerate(CatalogManager.catalog.get_type_list(tablename)):
					if i !='char':
						for r in res:
							r[cnt] = eval(r[cnt])
				for attribute in CatalogManager.catalog.get_column_with_index(tablename):
					attr_id = CatalogManager.catalog.get_the_index_of_attribute(tablename,attribute)
					for indexname in CatalogManager.catalog.get_index_name_by_seq(tablename,attr_id):
						IndexManager.index.delete_entries([x[attr_id] for x in res],tablename,indexname) 
				break
			if words[cnt+3] !='and':
				raise Exception('and expected but '+words[cnt+3]+' found.')
			cnt += 4