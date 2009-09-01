#!/usr/bin/python
# -*- coding: utf -*-

import os, time

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data


def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

writefile('settings/starttime',str(int(time.time())))

while 1:
	try: execfile('isida.py')
	except: time.sleep(1)
	if os.path.isfile('settings/tmp'): mode = str(readfile('settings/tmp'))
	if mode == 'update':
		os.system('echo `svnversion` > settings/ver')
		os.system('rm plugins/list.txt')
		os.system('svn up')
		os.system('echo `svnversion` > settings/version')
		try: ver = int(readfile('settings/version')[:3]) - int(readfile('settings/ver')[:3])
		except: ver = -1
		os.system('rm -r settings/ver')
		if ver > 0:	 os.system('svn log --limit '+str(ver)+' > update.log')
		elif ver < 0: os.system('echo Failed to detect version! > update.log')
		else: os.system('echo No Updates! > update.log')
	elif mode == 'exit': break
