#!/usr/bin/python
# -*- coding: utf -*-

import os, sys, sqlite3

set_folder = u'settings/'		# папка настроек
mainbase = set_folder+u'answers.db'	# основная база данных

print 'Autoanswer text to base convertor for Isida Jabber Bot'
print '(c) Disabler Production Lab.'

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

print 'Read textfile'
answer = readfile('answers.txt').decode('utf-8')
answer = answer.split('\n')

print 'Open and clean database'
mtb = os.path.isfile(mainbase)
mdb = sqlite3.connect(mainbase)
cu = mdb.cursor()
cu.execute('delete from answer where body like ?',('%',))

print 'Total records:',len(answer)
print 'Let\'s start!'
idx = 1
for i in answer:
	if i != '':
		cu.execute('insert into answer values (?,?)', (idx,unicode(i)))
		idx += 1
print 'Write base file'
mdb.commit()
print 'Finished!'
