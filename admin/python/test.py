from strhash import codeengine
a = codeengine.account('test',0)
#pwd = a.signup()[1]
salt = a.saltextract()
print('Salt is: ',salt)
b = a.codeblockextract(salt[0])
c = codeengine.decode(0)
c.decode(b['seed'],b['block'])

