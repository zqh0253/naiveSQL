import random

N = 38
fp = open('sql.txt','a+')
key = []

fp.seek(0)
fp.truncate()

fp.write ('create table qq (sid int,point float,primary key sid);\n')
for i in range(N):
	while 1:
		k = random.randint(1,10*N)
		if k not in key:
			key.append(k)
			break
	fp.write('insert into qq values ({},{});\n'.format(k,random.random()))			

for i in range(N//2):
	k = random.choice(key)
	fp.write('delete from qq where sid = {};\n'.format(k))
	key.remove(k)

fp.write ('select * from qq;\ndrop table qq;\n')
fp.close()

