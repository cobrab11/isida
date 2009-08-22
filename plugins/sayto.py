#!/usr/bin/python
# -*- coding: utf -*-

def sayto(type, jid, nick, text):
	if text.count(' '):
		to = text[:text.find(' ')]
		what = text[text.find(' ')+1:]
		frm = nick + '\n' + str(int(time.time()))
		merge_age()
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		fnd = cu.execute('select * from age where room=? and (nick=? or jid=?)',(jid,to,to)).fetchall()
		if len(fnd) == 1:
			fnd = fnd[0]
			if fnd[5]:
				msg = u'Передам'
				sdb = sqlite3.connect(saytobase)
				cu = sdb.cursor()
				cu.execute('insert into st values (?,?,?,?)', (frm, jid, fnd[2], what))
				sdb.commit()
			else: msg = u'Или я дура, или '+to+u' находится тут...'
		elif len(fnd) > 1: msg = u'Я видела несколько человек с таким ником. Укажите точнее!'
		else:
			msg = u'Я не в курсе кто такой '+to+u'. Могу не правильно передать.'
			sdb = sqlite3.connect(saytobase)
			cu = sdb.cursor()
			cu.execute('insert into st values (?,?,?,?)', (frm, jid, to, what))
			sdb.commit()
	else: msg = u'Кому что передать?'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'sayto', sayto, 2, u'Команда "передать".\nsayto jid|nick message - при входе в конференцию jid\'a или ника отправит сообщение "message"')]
