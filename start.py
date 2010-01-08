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

def tZ(val):
	val = str(val)
	if len(val) == 1: val = '0'+val
	return val

def printlog(text):
	print text
	lt = tuple(time.localtime())
	fname = 'log/crash_'+tZ(lt[0])+tZ(lt[1])+tZ(lt[2])+u'.txt'
	fbody = tZ(lt[3])+tZ(lt[4])+tZ(lt[5])+'|'+text+u'\n'
	fl = open(fname, 'a')
	fl.write(fbody.encode('utf-8'))
	fl.close()

if os.name == 'nt': printlog('Warning! Correct work only on *NIX system!')

try: writefile('settings/starttime',str(int(time.time())))
except:
	printlog('\n'+'*'*50+'\n Isida is crashed! Incorrent launch!\n'+'*'*50+'\n')
	raise

while 1:
	try: execfile('isida.py')
	except KeyboardInterrupt: break
	except Exception, SM:
		printlog('\n'+'*'*50+'\n Isida is crashed! It\'s imposible, but You do it!\n'+'*'*50+'\n')
		printlog(str(SM)+'\n')
		raise
	if os.path.isfile('settings/tmp'): mode = str(readfile('settings/tmp'))
	else:
		printlog('\nSystem error! Read user manual before start bot!')
		printlog('Try launch bot with debug mode.')
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
