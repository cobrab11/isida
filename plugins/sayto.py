#!/usr/bin/python
# -*- coding: utf -*-

last_cleanup_sayto_base = 0
sayto_timeout = 1209600

def sayto(type, jid, nick, text):
	if text.split(' ')[0] == 'show':
		try: text = text.split(' ',1)[1]
		except: text = ''
		ga = get_access(jid, nick)
		if ga[0] != 2: msg = u'Вам данная функция недоступна!'
		else:
			sdb = sqlite3.connect(saytobase)
			cu = sdb.cursor()
			cm = cu.execute('select * from st').fetchall()
			if len(cm):
				msg = u''
				for cc in cm:
					zz = cc[0].split('\n')
					tmsg = u'\n' + cc[1] +'/'+ zz[0] +' ('+un_unix(time.time()-int(zz[1]))+u'|'+un_unix(sayto_timeout-(time.time()-int(zz[1])))+u') для '+cc[2]+u' - '+cc[3]
					if len(text) and tmsg.lower().count(text.lower()): msg += tmsg
					elif not len(text): msg += tmsg
				if len(msg): msg = u'Не переданы сообщения:' + msg
				else: msg = u'Не найдено!'
				if type == 'groupchat':
					send_msg('chat', jid, nick, msg)
					msg = u'Отправила в приват!'
			else: msg = u'База пустая!'
	elif text.count(' '):
		to = text.split(' ')[0]
		what = text.split(' ',1)[1]
		frm = nick + '\n' + str(int(time.time()))
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		fnd = cu.execute('select status, jid from age where room=? and nick=? group by jid',(jid,to)).fetchall()
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
			if off_count: msg = u'Я видела несколько человек с таким ником и могу ошибочно передать. Совпадений: '+str(len(fnd))+u', будет передано сообщений: '+str(off_count)
			else: msg = u'Все, кого я видела с таким ником, находятся в конфе!'
		else:
			if to.count('@') and to.count('.'):
				fnd = cu.execute('select status, jid from age where room=? and jid=? group by jid',(jid,to)).fetchall()
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
			else: msg = u'Я не видела '+to+u' в конференции. Вы можете указать jid.'
	else: msg = u'Кому что передать?'
	send_msg(type, jid, nick, msg)

def sayto_presence(room,jid,nick,type,text):
	if nick != '':
		sdb = sqlite3.connect(saytobase)
		cu = sdb.cursor()
		cm = cu.execute('select * from st where room=? and (jid=? or jid=?)',(room, getRoom(jid), nick)).fetchall()
		if len(cm):
			cu.execute('delete from st where room=? and (jid=? or jid=?)',(room, getRoom(jid), nick))
			for cc in cm:
				if cc[0].count('\n'):
					zz = cc[0].split('\n')
					send_msg('chat', room, nick, zz[0]+' ('+un_unix(time.time()-int(zz[1]))+u' назад) просил передать: '+cc[3])
				else: send_msg('chat', room, nick, cc[0]+u' просил передать: '+cc[3])
			sdb.commit()

def cleanup_sayto_base():
	global last_cleanup_sayto_base
	ctime = int(time.time())
	if ctime-last_cleanup_sayto_base > 86400:
		last_cleanup_sayto_base = ctime
		sdb = sqlite3.connect(saytobase)
		cu = sdb.cursor()
		cm = cu.execute('select who, room, jid from st').fetchall()
		if len(cm):
			for cc in cm:
				if cc[0].count('\n'):
					tim = int(cc[0].split('\n')[1])
					if ctime-tim > sayto_timeout: cu.execute('delete from st where room=? and jid=?',(cc[1], cc[2]))
				else: cu.execute('delete from st where room=? and jid=?',(cc[1], cc[2]))
			sdb.commit()

def sayjid(type, jid, nick, text):
	try:
		text = text.split(' ',1)
		if len(text) != 2: msg = u'Ошибка'
		elif not text[0].count('@') and not text[0].count('@'): msg = u'Ошибка'
		elif not len(text[1]): msg = u'Ошибка'
		else: 
			send_msg(type, jid, nick, u'Отправила')
			msg = nick + u' из конференции ' + jid + u' передал: ' + text[1]
			type, nick, jid = 'chat', '', text[0]
	except: msg = u'Ошибка'
	send_msg(type, jid, nick, msg)
			
global execute, timer, presence_control

timer = [cleanup_sayto_base]
presence_control = [sayto_presence]
execute = [(0, u'sayto', sayto, 2, u'Команда "передать".\nsayto jid|nick message - при входе в конференцию jid\'a или ника отправит сообщение "message". Сообщения хронятся 14 дней, после чего недоставленные сообщения удаляются.'),
			(1, u'sayjid', sayjid, 2, u'Отправить сообщение на jid.\nsayjid jid message')]
