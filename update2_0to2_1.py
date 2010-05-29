# -*- coding: utf-8 -*- 

import os

set_folder 	= 'settings/'
fld = set_folder+'flood'
preffile = set_folder+'prefix'
sml = set_folder+'smile'
cns = set_folder+'censors'

config = {}

print 'Updater for Isida Jabber Bot from 2.00 to 2.10'
print '(c) Disabler Production Lab.'

def readfile(filename): return file(filename).read()
def writefile(filename, data): file(filename, 'w').write(data)
def getFile(filename,default):
	if os.path.isfile(filename):
		try: filebody = eval(readfile(filename))
		except:
			if os.path.isfile(filename+'.back'):
				while True:
					try:
						filebody = eval(readfile(filename+'.back'))
						break
					except: pass
			else:
				filebody = default
				writefile(filename,str(default))
	else:
		filebody = default
		writefile(filename,str(default))
	writefile(filename+'.back',str(filebody))
	return filebody

tempo = getFile(fld,[])
for tmp in tempo:
	tname = 'flood'
	try: t = config[tmp[0]]
	except: config[tmp[0]] = {}
	config[tmp[0]][tname] = tmp[1]
	
tempo = getFile(preffile,[])
for tmp in tempo:
	tname = 'prefix'
	try: t = config[tmp[0]]
	except: config[tmp[0]] = {}
	config[tmp[0]][tname] = tmp[1]

tempo = getFile(sml,[])
for tmp in tempo:
	tname = 'smile'
	try: t = config[tmp[0]]
	except: config[tmp[0]] = {}
	config[tmp[0]][tname] = tmp[1]
	
tempo = getFile(cns,[])
for tmp in tempo:
	tname = 'censor'
	try: t = config[tmp[0]]
	except: config[tmp[0]] = {}
	config[tmp[0]][tname] = tmp[1]

writefile(set_folder+'conference.config',str(config))
