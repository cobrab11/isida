#!/usr/bin/python
# -*- coding: utf -*-

import os, sys, sqlite3

set_folder = u'settings/'		# папка настроек
mainbase = set_folder+u'answers.db'	# основная база данных

print 'Autoanswer base to text convertor for Isida Jabber Bot'
print '(c) Disabler Production Lab.'

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

print 'Read database'
mtb = os.path.isfile(mainbase)
mdb = sqlite3.connect(mainbase)
cu = mdb.cursor()
base_size = len(cu.execute('select * from answer').fetchall())
fnd = cu.execute('select body from answer where body like ? group by body order by body',('%',)).fetchall()
answer = ''
print 'Total records:',base_size
print 'After remove duplicates:',len(fnd)
print 'Let\'s start!'
for i in fnd:
	if i[0] != '':
		answer += i[0].strip() +'\n'
print 'Write text file'
writefile('answers.txt',answer.encode('utf-8'))
print 'Finished!'
