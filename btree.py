import math
import json

root = {'is_leaf':True,'sons':[],'keys':[]}
N = 3

class Node():
	def __init__(self, is_leaf, keys, sons, parent = None):
		self.is_leaf = is_leaf
		self.keys = keys
		self.sons = sons
		self.parent = parent

	def ptr(self):
		print(self.keys)
		if self.is_leaf == False:
			# print(self.keys)
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
				tnode = tnode.sons[key]
				flag = True
		if flag == False:
			tnode = tnode.sons[-1]
	return tnode

def insert_into_leaf(node,_key,data):
	for index,key in enumerate(node.keys):
		if key == _key:
			raise Exception('Insertion fails. Data with key: '+str(key)+' already exists.')
		if key>_key:
			node.sons.insert(index,data)
			node.keys.insert(index,_key)
			return 
		node.sons.insert(len(node.sons),data)
		node.keys.insert(len(node.sons),_key)
		break	

def insert_into_parent(node1,node2):
	# print(node2.keys[0])
	if node1.parent==None:
		global treeroot
		parent_node = Node(False,[],[],None)
		treeroot = parent_node
	else:
		parent_node = node1.parent
	node2.parent = parent_node
	# print(node2.keys[0])
	parent_node.keys.append(node2.keys[0])
	parent_node.sons.append(node2)
	if len(parent_node.keys)==N-1:
		new_node=Node(False,[],[])
		up_key = parent_node.keys.pop(math.ceil((N+1)/2))
		for i in range(N-math.ceil((N)/2)):
			new_node.keys.append(parent_node.keys.pop(math.ceil((N)/2)))
			new_node.sons.append(parent_node.sons.pop(math.ceil((N)/2))+1)
		new_node.sons.append(parent_node.sons.pop(math.ceil((N)/2))+1)
		insert_into_parent(parent_node,new_node)

def insert(node,key,data):
	if len(node.keys)==0:
		node.keys.append(key)
		node.sons.append(data)
		return
	insert_node = find_leaf_place(node,key)
	if len(insert_node.keys)<N-1:
		insert_into_leaf(insert_node,key,data)
	else:
		insert_into_leaf(insert_node,key,data)
		new_node=Node(True,[],[])
		# print('---')
		for i in range(N-math.ceil(N/2)):
			# print((insert_node.keys))
			new_node.keys.append(insert_node.keys.pop(math.ceil(N/2)))
			new_node.sons.append(insert_node.sons.pop(math.ceil(N/2)))
		# print(insert_node.keys,new_node.keys)
		insert_into_parent(insert_node,new_node)

treeroot = load_tree_from_json(root)
while(1):
	a = int(input())
	if a == -1:
		break
	else:
		insert(treeroot,a,'x')
		print(save_tree_into_json(treeroot))