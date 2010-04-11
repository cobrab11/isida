#!/usr/bin/python
# -*- coding: utf -*-

import os, sys, sqlite3

set_folder = u'settings/'		# папка настроек
agestatfile = set_folder+u'agestat'	# статистика возрастов
jidbasefile = set_folder+u'jidbase'	# статистика jid'ов
talkersfile = set_folder+u'talkers'	# статистика болтунов
wtfbasefile = set_folder+u'wtfbase'	# определения
answersfile = set_folder+u'answers'	# ответы бота

mainbase = set_folder+u'main.db'	# основная база данных

print 'Updater for Isida Jabber Bot from 0.6 to 0.7'
print '(c) Disabler Production Lab.'

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

if os.path.isfile(mainbase):
	print 'Remove previos base'
	os.system('rm -r '+mainbase)

print 'Create new base'
mtb = os.path.isfile(mainbase)
mdb = sqlite3.connect(mainbase)
cu = mdb.cursor()

cu.execute('''create table age (room text, nick text, jid text, time integer, age integer, status integer, type text, message text)''')
cu.execute('''create table answer (ind integer, body text)''')
cu.execute('''create table jid (login text, server text, resourse text)''')
cu.execute('''create table talkers (room text, jid text, nick text, words integer, frases integer)''')
cu.execute('''create table wtf (ind integer, room text, jid text, nick text, wtfword text, wtftext text, time text)''')

print 'Done'

if os.path.isfile(agestatfile):
	agestat = eval(readfile(agestatfile))
	print 'Import age statistic ...', len(agestat)
	for aa in agestat:
		cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],'',''))

if os.path.isfile(answersfile):
	answers = eval(readfile(answersfile))
	print 'Import auto-answer base ...', len(answers)
	cnt = 1
	for aa in answers:
		cu.execute('insert into answer values (?,?)', (cnt,aa[0]))
		cnt += 1
else:
	print 'Create defaul auto-answer base'
	cu.execute('insert into answer values (?,?)', (1,u';-)'))
	cu.execute('insert into answer values (?,?)', (2,u'Привет'))

if os.path.isfile(jidbasefile):
	jidbase = eval(readfile(jidbasefile))
	print 'Import jid base ...', len(jidbase)
	for aa in jidbase:
		aa1 = aa[:aa.index('@')]
		aa2 = aa[aa.index('@')+1:aa.index('/')]
		aa3 = aa[aa.index('/')+1:]
		cu.execute('insert into jid values (?,?,?)', (aa1,aa2,aa3))

if os.path.isfile(talkersfile):
	talkers = eval(readfile(talkersfile))
	print 'Import age statistic ...', len(talkers)
	for aa in talkers:
		cu.execute('insert into talkers values (?,?,?,?,?)', (aa[0],aa[1],aa[2],aa[3],aa[4]))

if os.path.isfile(wtfbasefile):
	cnt = 1
	wtfbase = eval(readfile(wtfbasefile))
	print 'Import wtf base ...', len(wtfbase)
	for aa in wtfbase:
		cu.execute('insert into wtf values (?,?,?,?,?,?,?)', (cnt,aa[0],aa[1],aa[2],aa[3],aa[4],aa[5]))
		cnt += 1

mdb.commit()
print 'Finished!'
