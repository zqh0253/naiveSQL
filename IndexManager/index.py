import os
import math
import json
import CatalogManager.catalog

path = 'D:/work/cs/db/minisql/naiveSQL/dbfile/index/'
fp = {}
treeroot = {}
root = None
N = 4

class Node():
	def __init__(self, is_leaf, keys, sons, parent = None, left = None, right = None):
		self.is_leaf = is_leaf
		self.keys = keys
		self.sons = sons
		self.parent = parent
		self.left = left
		self.right = right


	def ptr(self):
		print(self.keys)
		if self.is_leaf == False:
			for x in self.sons:
				x.ptr()
	
def load_tree_from_json(j,parent=None):
	if j['is_leaf']==True:
		node = Node(j['is_leaf'],j['keys'],j['sons']) 
	else:
		node = Node(j['is_leaf'],j['keys'],[create_tree_from_json(x) for x in j['sons']])
		for son in node.sons:
			son.parent = node
	return node

def save_tree_into_json(j):
	m = {}
	m['is_leaf'] = j.is_leaf
	m['keys'] = j.keys
	m['sons'] = [(save_tree_into_json(x)) for x in j.sons] if m['is_leaf']==False else j.sons
	return m

def find_leaf_place(node,value):
	tnode = node
	while not tnode.is_leaf:
		flag = False
		for index, key in enumerate(tnode.keys):
			if key>value:
				tnode = tnode.sons[index]
				flag = True
				break
		if flag == False:
			tnode = tnode.sons[-1]
	return tnode

def insert_into_leaf(node,_key,data,is_insert = True):
	for index,key in enumerate(node.keys):
		if key == _key:
			if not is_insert:
				return node.sons[index]
			else:
				print(key,'>>>>', _key)
				raise Exception(_key)
		if is_insert and key>_key:
			node.sons.insert(index,data)
			node.keys.insert(index,_key)
			return None
	if is_insert:
		node.sons.insert(len(node.sons),data)
		node.keys.insert(len(node.sons),_key)
		return None

def insert_into_parent(node1,node2):
	if node1.parent==None:
		# global treeroot
		# parent_node = Node(False,[],[],None)
		# treeroot = parent_node
		# parent_node.sons.append(node1)
		# node1.parent =parent_node

		global root
		parent_node = Node(False,[],[],None)
		root = parent_node
		parent_node.sons.append(node1)
		node1.parent =parent_node

	else:
		parent_node = node1.parent
	id = get_id(parent_node, node1)
	node2.parent = parent_node
	if node1.is_leaf==False:
		parent_node.keys.insert(id,node2.keys.pop(0))
	else:
		parent_node.keys.insert(id,node2.keys[0])
	parent_node.sons.insert(id+1,node2)
	if len(parent_node.keys)==N:
		new_node=Node(False,[],[])
		for i in range(N-math.ceil((N-1)/2)):
			new_node.keys.append(parent_node.keys.pop(math.ceil((N-1)/2)))
			new_node.sons.append(parent_node.sons.pop(math.ceil((N-1)/2)+1))
		for x in new_node.sons:
			x.parent = new_node
		new_node.right = parent_node.right
		if parent_node.right !=None:
			parent_node.right.left = new_node
		parent_node.right = new_node
		new_node.left = parent_node
		insert_into_parent(parent_node,new_node)

def insert(node,key,data,is_insert = True):
	if len(node.keys)==0:
		node.keys.append(key)
		node.sons.append(data)
		return []
	insert_node = find_leaf_place(node,key)
	if len(insert_node.keys)<N-1:
		res = insert_into_leaf(insert_node,key,data,is_insert)
		if res != None:
			return res
	else:
		res = insert_into_leaf(insert_node,key,data,is_insert)
		if res != None:
			return res
		new_node=Node(True,[],[])
		for i in range(N-math.ceil((N-1)/2)):
			new_node.keys.append(insert_node.keys.pop(math.ceil((N-1)/2)))
			new_node.sons.append(insert_node.sons.pop(math.ceil((N-1)/2)))
		new_node.right = insert_node.right
		if insert_node.right != None:
				insert_node.right.left = new_node
		insert_node.right = new_node
		new_node.left = insert_node
		insert_into_parent(insert_node,new_node)
	return []

def get_id(f_node, node):
	for index,n in enumerate(f_node.sons):
		if n == node:
			return index
	raise Exception('fuck your get_id')

def delete_node(node, index):
	least = math.ceil((N)/2) - 1
	node.keys.pop(index)
	node.sons.pop(index+1)

	if len(node.keys) >= least:
		return
	if node.parent==None:
		if len(node.keys)==0 and len(node.sons[0].keys)!=0:
			global root
			root = node.sons[0]
			node.sons[0].parent = None		
		return 
	if node.parent.sons[0]==node:
		id = get_id(node.parent, node)
		if len(node.parent.sons[1].keys) >least:
			node.keys.append(node.parent.keys[id])
			node.parent.keys[id] = node.parent.sons[1].keys.pop(0)
			node.sons.append(node.parent.sons[1].sons.pop(0))
			node.sons[-1].parent = node
		else:
			node.keys.append(node.parent.keys[id])
			for i in range(len(node.parent.sons[1].keys)):
				node.keys.append((node.parent.sons[1].keys[i]))
				node.sons.append((node.parent.sons[1].sons[i]))
				node.sons[-1].parent = node
			node.sons.append((node.parent.sons[1].sons[-1]))
			node.sons[-1].parent = node
			if node.right.right!=None:
				node.right.right.left = node
			node.right = node.right.right
			delete_node(node.parent,id)
	else:
		id = get_id(node.parent, node) - 1
		if len(node.parent.sons[id].keys)>least:
			node.keys.insert(0,node.parent.keys[id])
			node.parent.keys[id] = node.parent.sons[id].keys.pop(-1)
			node.sons.insert(0,node.parent.sons[id].sons.pop(-1))
			node.sons[0].parent = node
		else:
			node.parent.sons[id].keys.append(node.parent.keys[id])
			for i in range(len(node.keys)):
				node.parent.sons[id].keys.append(node.keys[i])
				node.parent.sons[id].sons.append(node.sons[i])
				node.parent.sons[id].sons[-1].parent = node.parent.sons[id]
			node.parent.sons[id].sons.append(node.sons[-1])
			node.parent.sons[id].sons[-1].parent = node.parent.sons[id]
			if node.right!=None:
				node.right.left = node.left
			node.left.right = node.right
			delete_node(node.parent,id)

def delete(node,key):
	cur_node = find_leaf_place(node,key)
	flag = True
	least = math.ceil((N-1)/2)
	for index,_key in enumerate(cur_node.keys):
		if key == _key:
			flag = False
			cur_node.sons.pop(index)
			cur_node.keys.pop(index)
			break
	if flag:
		raise Exception('No point to delete')
	if cur_node.parent!=None and len(cur_node.keys)<least:
		# print(cur_node.parent.sons[0],cur_node)
		if cur_node.parent.sons[0]==cur_node:
			if len(cur_node.parent.sons[1].keys)>least:
				cur_node.sons.append(cur_node.parent.sons[1].sons.pop(0))
				cur_node.keys.append(cur_node.parent.sons[1].keys.pop(0))
				cur_node.parent.keys[0] = cur_node.parent.sons[1].keys[0]
			else:
				for i in range(len(cur_node.parent.sons[1].keys)):
					cur_node.sons.append(cur_node.parent.sons[1].sons[i])
					cur_node.keys.append(cur_node.parent.sons[1].keys[i])
				if cur_node.right.right!=None:
					cur_node.right.right.left = cur_node
				cur_node.right = cur_node.right.right
				delete_node(cur_node.parent,0)
		else:
			id = get_id (cur_node.parent,cur_node) - 1
			if len(cur_node.parent.sons[id].keys)>least:
				cur_node.sons.insert(0,cur_node.parent.sons[id].sons.pop(-1))
				cur_node.keys.insert(0,cur_node.parent.sons[id].keys.pop(-1))
				cur_node.parent.keys[id] = cur_node.keys[0]
			else:
				for i in range(len(cur_node.keys)):
					cur_node.parent.sons[id].sons.append(cur_node.sons[i])
					cur_node.parent.sons[id].keys.append(cur_node.keys[i])
				if cur_node.right!=None:
					cur_node.right.left = cur_node.left
				cur_node.left.right = cur_node.right
				delete_node(cur_node.parent,id)

def get_leftest_child(node):
	tnode = node
	while not tnode.is_leaf:
		tnode = tnode.sons[0] 
	return tnode

def print_list(node):
	for x in node.keys:
		print(x,end=' ')
	if node.right!=None:
		print_list(node.right)

prev = None
def maintain_left_right_pointer(node):
	global prev
	if node!=None:
		if node.is_leaf:
			if prev!=None:
				prev.right = node
				node.left = prev
			prev = node
		else:
			for x in node.sons:
				maintain_left_right_pointer(x)
	node.right = None

def get_rightest_child(node):
	tnode = node
	while not tnode.is_leaf:
		tnode = tnode.sons[-1]
	return tnode
	
def print_l_list(node):
	for x in reversed(node.keys):
		print(x,end=' ')
	if node.left != None:	
		print_l_list(node.left)

def init():
	file_list = os.listdir(path)
	for file in file_list:
		fp[file.rstrip('.ind')] = open(path+file,'a+')
		fp[file.rstrip('.ind')].seek(0)
		treeroot[file.rstrip('.ind')]=load_tree_from_json(json.loads(fp[file.rstrip('.ind')].read()))
		global prev 
		prev = None
		maintain_left_right_pointer(treeroot[file.rstrip('.ind')])

def finalize():
	file_list = os.listdir(path)
	for file in file_list:
		name = file.rstrip('.ind') 
		fp[name].seek(0)
		fp[name].truncate()
		fp[name].write(json.dumps(save_tree_into_json(treeroot[name])))
		fp[name].close()

def create_table(tablename,indexname):
	p = open(path+tablename+'_'+indexname+'.ind','a+')
	fp[tablename+'_'+indexname] = p
	fp[tablename+'_'+indexname].write('{"is_leaf":true,"sons":[],"keys":[]}')
	treeroot[tablename+'_'+indexname]=load_tree_from_json(json.loads('{"is_leaf":true,"sons":[],"keys":[]}'))
	global prev 
	prev = None
	maintain_left_right_pointer(treeroot[tablename+'_'+indexname])

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
	raise Exception('No index named '+indexname+'.')

def create_index(tablename, indexname, res):
	fp[tablename+'_'+indexname] = open(path+tablename+'_'+indexname+'.ind','a+')
	fp[tablename+'_'+indexname].write('{"is_leaf":true,"sons":[],"keys":[]}')
	treeroot[tablename+'_'+indexname]=load_tree_from_json(json.loads('{"is_leaf":true,"sons":[],"keys":[]}'))
	global prev 
	prev = None
	maintain_left_right_pointer(treeroot[tablename+'_'+indexname])	
	for r in res:
		key = r[1]
		data = r[0]
		insert_entry(tablename,indexname,key,data)
		
def insert_entry(tablename,indexname, key, data):
	global root
	root = treeroot[tablename+'_'+indexname]
	res = insert(treeroot[tablename+'_'+indexname],key,data)
	treeroot[tablename+'_'+indexname] = root
	# prt(get_leftest_child(treeroot[tablename+'_'+indexname]))
	# print('---------------------------')
	# prtl(get_rightest_child(treeroot[tablename+'_'+indexname]))

def select(tablename, clause, indexname):
	res,value = [],eval(clause[2])
	if clause[1]=='!=':
		res = get_data_list_right(get_leftest_child(treeroot[tablename+'_'+indexname]), value)
	elif clause[1]=='==':
		res.append( insert(treeroot[tablename+'_'+indexname],eval(clause[2]),None,False))
	else:
		break_block = find_leaf_place(treeroot[tablename+'_'+indexname],value)
		for index, key in enumerate(break_block.keys):
			if eval('key' + clause[1] + clause[2]):
				res.append(break_block.sons[index])
		if '>' in clause[1] and break_block.right != None:
			res += get_data_list_right(break_block.right)
		elif '<' in clause[1] and break_block.left != None:
			res += get_data_list_left(break_block.left)
	return res

def delete_all(tablename, indexname):
	treeroot[tablename+'_'+indexname] = load_tree_from_json(json.loads('{"is_leaf":true,"sons":[],"keys":[]}'))
	global prev
	prev = None
	maintain_left_right_pointer(treeroot[tablename+'_'+indexname])

def delete_entries(keylist, tablename, indexname):
	for key in keylist:
		global root
		root = treeroot[tablename+'_'+indexname]
		delete(treeroot[tablename+'_'+indexname],key)
		treeroot[tablename+'_'+indexname] = root