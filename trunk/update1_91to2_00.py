#!/usr/bin/python
# -*- coding: utf -*-

import os, sys, sqlite3

set_folder = u'settings/'				# папка настроек

wtfbase = set_folder+u'wtfbase.db'		# старые определения
wtfbase2 = set_folder+u'wtfbase2.db'	# новые определения

print 'Updater for Isida Jabber Bot from 1.8-1.91 to 2.00'
print '(c) Disabler Production Lab.'

os.system('rm -rf '+wtfbase2)

wtf1 = sqlite3.connect(wtfbase)
cu_wtf1 = wtf1.cursor()

wtf2 = sqlite3.connect(wtfbase2)
cu_wtf2 = wtf2.cursor()
cu_wtf2.execute('''create table wtf (ind integer, room text, jid text, nick text, wtfword text, wtftext text, time text, lim integer)''')

tmp = cu_wtf1.execute('select * from wtf').fetchall()
print 'Import wtf base ...', len(tmp)
for aa in tmp:
	if aa[1] == 'global': aa += (5,)
	else: aa += (0,)
	cu_wtf2.execute('insert into wtf values (?,?,?,?,?,?,?,?)', aa)
wtf2.commit()
wtf2.close()
wtf1.close()

print 'Finished!'
