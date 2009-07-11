#!/usr/bin/python
# -*- coding: utf -*-
#
# Launch this script after any modificaion on censor.txt
#

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

cens = u'censor.txt'

if os.path.isfile(cens):
	censor = readfile(cens).decode('utf-8')

	cn = ''
	for c in censor:
		if ord(c) != 10:
			cn += c
		else:
			cn += chr(13)
	writefile(cens, cn.encode('utf-8'))
	print 'Done'
else:
	print cens+' not found!'
