#!/usr/bin/python
# -*- coding: utf -*-
#
# Launch this script after any modificaion on censor.txt
#

def readfile(filename): return file(filename).read()
def writefile(filename, data): file(filename, 'w').write(data)

cens = u'censor.txt'

if os.path.isfile(cens):
	censor = readfile(cens).decode('utf-8')
	cn = ''
	for c in censor:
		if ord(c) != 10: cn += c
		else: cn += chr(13)
	writefile(cens, cn.encode('utf-8'))
	print 'Done'
else: print '%s not found!' % cens
