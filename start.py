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

if os.name == 'nt': print 'Warning! Correct work only on *NIX system!'

try: writefile('settings/starttime',str(int(time.time())))
except:
	print '\n','*'*50,'\n Isida is crashed! Incorrent launch!\n','*'*50,'\n'
	raise

while 1:
	try: execfile('isida.py')
	except:
		print '\n','*'*50,'\n Isida is crashed! It\'s imposible, but You do it!\n','*'*50,'\n'
		raise
	if os.path.isfile('settings/tmp'): mode = str(readfile('settings/tmp'))
	else:
		print '\nSystem error! Read user manual before start bot!'
		print 'Try launch bot with debug mode.'
		break
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
