import math
import json

root = {'is_leaf':True,'sons':[],'keys':[]}
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

def insert_into_leaf(node,_key,data,is_insert = False):
	for index,key in enumerate(node.keys):
		if key == _key:
			raise Exception('Insertion fails. Data with key: '+str(key)+' already exists.')
		if key>_key:
			node.sons.insert(index,data)
			node.keys.insert(index,_key)
			return 
	node.sons.insert(len(node.sons),data)
	node.keys.insert(len(node.sons),_key)

def insert_into_parent(node1,node2):
	if node1.parent==None:
		global treeroot
		parent_node = Node(False,[],[],None)
		treeroot = parent_node
		parent_node.sons.append(node1)
		node1.parent =parent_node

		# global root
		# parent_node = Node(False,[],[],None)
		# root = parent_node
		# parent_node.sons.append(node1)
		# node1.parent =parent_node

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

def insert(node,key,data,is_insert = False):
	if len(node.keys)==0:
		node.keys.append(key)
		node.sons.append(data)
		return
	insert_node = find_leaf_place(node,key)
	if len(insert_node.keys)<N-1:
		insert_into_leaf(insert_node,key,data,is_insert)
	else:
		insert_into_leaf(insert_node,key,data,is_insert)
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

def get_id(f_node, node):
	for index,n in enumerate(f_node.sons):
		if n == node:
			return index
	raise Exception('fuck your get_id')

def delete_node(node, index):
	least = math.ceil((N-1)/2)
	node.keys.pop(index)
	node.sons.pop(index+1)
	if len(node.keys) >= least:
		return
	if node.parent==None:
		if len(node.keys)==0 and len(node.sons[0].keys)!=0:
			global treeroot
			treeroot = node.sons[0]
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
			node.right = node.right.right
			delete_node(node.parent,id)
	else:
		id = get_id(node.parent, node) - 1
		if len(node.parent.sons[id].keys)>least:
			node.keys.insert(0,node.parent.keys[id])
			node.parent.keys[id] = node.parent.sons[id].keys.pop(-1)
			node.sons.insert(0,node.parent.sons[id].pop(-1))
			node.sons[0].parent = node
		else:
			node.parent.sons[id].keys.append(node.parent.keys[id])
			for i in range(len(node.keys)):
				node.parent.sons[id].keys.append(node.keys[i])
				node.parent.sons[id].sons.append(node.sons[i])
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
			print('A')
			if len(cur_node.parent.sons[1].keys)>least:
				cur_node.sons.append(cur_node.parent.sons[1].sons.pop(0))
				cur_node.keys.append(cur_node.parent.sons[1].keys.pop(0))
				cur_node.parent.keys[0] = cur_node.parent.sons[1].keys[0]
			else:
				for i in range(len(cur_node.parent.sons[1].keys)):
					cur_node.sons.append(cur_node.parent.sons[1].sons[i])
					cur_node.keys.append(cur_node.parent.sons[1].keys[i])
				cur_node.right = cur_node.right.right
				delete_node(cur_node.parent,0)
		else:
			print('B')
			id = get_id (cur_node.parent,cur_node) - 1
			if len(cur_node.parent.sons[id].keys)>least:
				cur_node.sons.insert(0,cur_node.parent.sons[id].sons.pop(-1))
				cur_node.keys.insert(0,cur_node.parent.sons[id].keys.pop(-1))
				cur_node.parent.keys[id] = cur_node.keys[0]
			else:
				print('here',id)
				for i in range(len(cur_node.keys)):
					cur_node.parent.sons[id].sons.append(cur_node.sons[i])
					cur_node.parent.sons[id].keys.append(cur_node.keys[i])
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

treeroot = load_tree_from_json(root)
while(1):
	b= int(input())
	a = int(input())
	if a == -1:
		break
	else:
		if b==1:
			insert(treeroot,a,-a)
		else:
			delete(treeroot,a)
		# maintain_left_right_pointer(treeroot)
		print(save_tree_into_json(treeroot))
		print_list(get_leftest_child(treeroot))
		print('----------------------')
		print_l_list(get_rightest_child(treeroot))
		print()