#!/usr/bin/python
# -*- coding: utf -*-

def sayto(type, jid, nick, text):
	if text.count(' '):
		to = text.split(' ')[0]
		what = text.split(' ',1)[1]
		frm = nick + '\n' + str(int(time.time()))
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		fnd = cu.execute('select status, jid from age where room=? and nick=? group by jid ',(jid,to)).fetchall()
		if len(fnd) == 1:
			fnd = fnd[0]
			if fnd[0]:
				msg = u'Передам'
				sdb = sqlite3.connect(saytobase)
				cu = sdb.cursor()
				cu.execute('insert into st values (?,?,?,?)', (frm, jid, fnd[1], what))
				sdb.commit()
			else: msg = u'Или я дура, или '+to+u' находится тут...'
		elif len(fnd) > 1:
			off_count = 0
			sdb = sqlite3.connect(saytobase)
			cu = sdb.cursor()
			for tmp in fnd:
				if tmp[0]:
					cu.execute('insert into st values (?,?,?,?)', (frm, jid, tmp[1], what))
					off_count += 1
			sdb.commit()
			if off_count: msg = u'Я видела несколько человек с таким ником и могу ошибочно передать. Совпадений: '+str(len(fnd))+u', будет передано: '+str(off_count)
			else: msg = u'Все, кого я видела с таким ником, находятся в конфе!'
		else:
			if to.count('@') and to.count('.'):
				fnd = cu.execute('select status, jid from age where room=? and jid=? group by jid ',(jid,to)).fetchall()
				sdb = sqlite3.connect(saytobase)
				cu = sdb.cursor()
				if fnd:
					off_count = 0
					for tmp in fnd:
						if tmp[0]:
							cu.execute('insert into st values (?,?,?,?)', (frm, jid, tmp[1], what))
							off_count += 1
					if off_count: msg = u'Передам'
					else: msg = u'Данный jid находится в конфе!'
				else:
					msg = u'Я не видела человека с jid\'ом '+to+u', но если зайдёт - я передам.'
					cu.execute('insert into st values (?,?,?,?)', (frm, jid, to, what))
				sdb.commit()
			else: msg = u'Я не видела '+to+u'в конференции. Вы можете указать jid.'
	else: msg = u'Кому что передать?'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'sayto', sayto, 2, u'Команда "передать".\nsayto jid|nick message - при входе в конференцию jid\'a или ника отправит сообщение "message"')]
