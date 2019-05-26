import re

def create(args):
	args = re.sub(r' +', ' ', args).strip().replace('\u200b','')
	words = [word for word in re.split(' |\(|\)|,',args) if word!='']
	print(words)
	if words[1] == 'table':
		tablename,attributes,cnt,length,primary = words[2],[],3,len(words),None
		while (1):
			unique = 0
			if words[cnt]=='primary':
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
					attributes.append([words[cnt], words[cnt+1], 0, unique])
					cnt += (2+unique)
				else:
					if cnt + 2 == length:
						raise Exception("maximum length of char expected.")
					if cnt + 3 < length and words[cnt+3]=='unique':
						unique = 1
					attributes.append([words[cnt], words[cnt+1], int(words[cnt+2]), unique])
					cnt += (3+unique)
			if cnt  == length:
				print(attributes,primary,tablename)
				# ...
				break
	elif words[1] == 'index':
		if len(words)!=6 or words[3]!='on':
			raise Exception("Syntax error. It should be: create index [index's name] on [tablename] ([columnname])")
		print(words[2],words[4],words[5])
	else:
		raise Exception('[table/index] expected, but '+words[2]+' found.')

def drop(args):
	args = re.sub(r' +', ' ', args).strip().replace('\u200b','')
	words = [word for word in re.split(' |\(|\)|,',args) if word!='']
	if words[1]=='table':
		print(words[2])
	elif words[1]=='index':
		print(words[2])
	else:
		raise Exception('[table/index] expected, but '+words[2]+' found.')