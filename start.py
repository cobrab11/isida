#!/usr/bin/python
# -*- coding: utf -*-

import os

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

while 1:
	execfile('isida.py')
	if os.path.isfile('settings/tmp'):
		mode = str(readfile('settings/tmp'))
	if mode == 'update':
		os.system('svn up')
		os.system('echo `svnversion` > settings/version')
	elif mode == 'exit':
		break
            
