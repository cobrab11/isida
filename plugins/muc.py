#!/usr/bin/python
# -*- coding: utf -*-

tban = set_folder+u'temporary.ban'		# лог временного бана
af_alist = set_folder+u'alist.aff'		# alist аффиляций
ro_alist = set_folder+u'alist.rol'		# alist ролей

# -------------- affiliation -----------------

def muc_tempo_ban(type, jid, nick,text):
	if text[:4].lower() == 'show' and not text.count('\n'):
		text = text[5:]
		if not len(text):
			text = '.'
		ubl = getFile(tban,[])
		msg = u''
		for ub in ubl:
			if ub[0] == jid and ub[1].count(text.lower()):
				msg += u'\n'+ub[1]+u'\t'+un_unix(ub[2]-int(time.time()))
		if len(msg):
			msg = u'Найдено:'+msg
		else:
			msg = u'Не найдено!'
		send_msg(type, jid, nick, msg)

	elif text[:3].lower() == 'del' and not text.count('\n'):
		text = text[4:]
		if not len(text):
			text = '@@'
		ubl = getFile(tban,[])
		msg = u''
		for ub in ubl:
			if ub[0] == jid and ub[1] == text.lower():
				msg += ub[1]+u'\t'+un_unix(ub[2]-int(time.time()))
				iqid = str(randint(1,100000))
				i = Node('iq', {'id': iqid, 'type': 'set', 'to':ub[0]}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'none', 'jid':getRoom(unicode(ub[1]))},[])])])
				cl.send(i)
				ubl.remove(ub)
		if len(msg):
			msg = u'Удалено: '+msg
			writefile(tban,str(ubl))
		else:
			msg = u'Не найдено!'
		send_msg(type, jid, nick, msg)

	else:
		muc_tempo_ban2(type, jid, nick,text)

def muc_tempo_ban2(type, jid, nick,text):
	skip = 1
	if len(text):
		who = text.split('\n',2)[0]
		try:
			ttime = text.split('\n',2)[1]
			tttime = int(ttime[:-1])
			tmode = ttime[-1:].lower()
			tkpd = {'s':1, 'm':60, 'h':3600, 'd':86400}
			tttime = tttime*tkpd[tmode]
		except:
			tttime = 0

		if tttime:
			try:
				reason = text.split('\n',2)[2]
			except:
				reason = u'No reason!'

			reason = u'бан сроком '+un_unix(tttime)+u', начиная с '+timeadd(tuple(localtime()))+u', по причине: '+reason
			mdb = sqlite3.connect(agestatbase)
			cu = mdb.cursor()
			fnd = cu.execute('select jid from age where room=? and (nick=? or jid=?)',(jid,who,who)).fetchall()
			if len(fnd) == 1:
				msg = u'done'
				whojid = getRoom(unicode(fnd[0][0]))
				skip = 0
			elif len(fnd) > 1:
				msg = u'Я видела несколько человек с таким ником. Укажите точнее!'
			else:
				if who.count('.'):
					msg = u'Я не в курсе кто такой '+who+u' и баню как есть!'
					whojid = who
					skip = 0
				else:
					msg = u'Я не в курсе кто такой '+who
		else:
			msg = u'Ошибка формата времени!'
	else:
		msg = u'Ась?'

	if skip:
		send_msg(type, jid, nick, msg)
	else:
		iqid = str(randint(1,100000))
		i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'outcast', 'jid':unicode(whojid)},[Node('reason',{},reason)])])])
		cl.send(i)

		ubl = getFile(tban,[])
		for ub in ubl:
			if ub[0] == jid and ub[1] == whojid:
				ubl.remove(ub)
		ubl.append((jid,whojid,tttime+int(time.time())))
		writefile(tban,str(ubl))
		send_msg(type, jid, nick, msg)

def muc_ban(type, jid, nick,text):
	muc_affiliation(type, jid, nick, text, 'outcast')

def muc_none(type, jid, nick,text):
	muc_affiliation(type, jid, nick, text, 'none')

def muc_member(type, jid, nick,text):
	muc_affiliation(type, jid, nick, text, 'member')

def muc_admin(type, jid, nick,text):
	muc_affiliation(type, jid, nick, text, 'admin')

def muc_owner(type, jid, nick,text):
	muc_affiliation(type, jid, nick, text, 'owner')

def muc_affiliation(type, jid, nick, text, aff):
	tmppos = arr_semi_find(confbase, jid)
	if tmppos == -1:
		nowname = nickname
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '':
			nowname = nickname
	xtype = ''
	for base in megabase:
		if base[0].lower() == jid and base[1] == nowname:
			xtype = base[3]
			break
	if xtype == 'owner':
		msg = u'Команда блокирована!'
		text = ''
	else:
		msg = u'Ась?'
	skip = 1
	if len(text):
		if text.count('\n'):
			who = text.split('\n',1)[0]
			reason = text.split('\n',1)[1]
		else:
			who = text
			reason = u'by Isida!'
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		fnd = cu.execute('select jid from age where room=? and (nick=? or jid=?)',(jid,who,who)).fetchall()
		if len(fnd) == 1:
			msg = u'done'
			whojid = getRoom(unicode(fnd[0][0]))
			skip = 0
		elif len(fnd) > 1:
			msg = u'Я видела несколько человек с таким ником. Укажите точнее!'
		else:
			msg = u'Я не в курсе кто такой '+who+u' и использую как есть!'
			whojid = who
			skip = 0
	if skip:
		send_msg(type, jid, nick, msg)
	else:
		iqid = str(randint(1,100000))
		i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':aff, 'jid':unicode(whojid)},[Node('reason',{},reason)])])])
		cl.send(i)
		send_msg(type, jid, nick, msg)

# -------------- role -----------------

def muc_kick(type, jid, nick,text):
	muc_role(type, jid, nick, text, 'none')

def muc_participant(type, jid, nick,text):
	muc_role(type, jid, nick, text, 'participant')

def muc_visitor(type, jid, nick,text):
	muc_role(type, jid, nick, text, 'visitor')

def muc_moderator(type, jid, nick,text):
	muc_role(type, jid, nick, text, 'moderator')

def muc_role(type, jid, nick, text, role):
	skip = 1
	if len(text):
		if text.count('\n'):
			who = text.split('\n',1)[0]
			reason = text.split('\n',1)[1]
		else:
			who = text
			reason = u'by Isida!'
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		fnd = cu.execute('select nick from age where room=? and (nick=? or jid=?)',(jid,who,who)).fetchall()
		if len(fnd) == 1:
			whonick = unicode(fnd[0][0])
			msg = u'done'
			skip = 0
		elif len(fnd) > 1:
			msg = u'Я видела несколько человек с таким ником. Укажите точнее!'
		else:
			msg = u'Я не в курсе кто такой '+who+u' и использую как есть!'
			whonick = who
			skip = 0
	else:
		msg = u'Ась?'

	if skip:
		send_msg(type, jid, nick, msg)
	else:
		iqid = str(randint(1,100000))
		i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':role, 'nick':unicode(whonick)},[Node('reason',{},reason)])])])
		cl.send(i)
		send_msg(type, jid, nick, msg)

# ----------------------------------------------
# role nick
# time
# reason
def muc_akick(type, jid, nick,text):
	muc_arole(type, jid, nick, text, 'none')

def muc_aparticipant(type, jid, nick,text):
	muc_arole(type, jid, nick, text, 'participant')

def muc_avisitor(type, jid, nick,text):
	muc_arole(type, jid, nick, text, 'visitor')

def muc_amoderator(type, jid, nick,text):
	muc_arole(type, jid, nick, text, 'moderator')

def muc_arole(type, jid, nick, text, role):
	skip = 1
	if len(text):
		if text[:4].lower() == 'show' and not text.count('\n'):
			text = text[5:]
			if not len(text):
				text = '.'
			alist_role = getFile(ro_alist,[])
			msg = u''
			if alist_role != '[]':
				for tmp in alist_role:
					if tmp[0] == jid and tmp[3] == role and tmp[2].count(text.lower()):
						msg += u'\n'+tmp[2]+'\t'+tmp[4]+' (by '+tmp[1]+')'
						if tmp[5]:
							msg += '\t'+un_unix(tmp[5]-int(time.time()))
			if not len(msg):
				if text == '.':
					msg = u'Список пуст!'
				else:
					msg = u'Не найдено!'

		elif text[:4].lower() == 'del ' and not text.count('\n'):
			text = text[4:]
			if not len(text):
				msg = u'Кого удалить?'
			else:
				msg = u'Не найдено'
				alist_role = getFile(ro_alist,[])
				for tmp in alist_role:
					if tmp[0] == jid and (tmp[1] == text or tmp[2] == text):
						alist_role.remove(tmp)
						writefile(ro_alist,str(alist_role))
						msg = u'Удалено: '+tmp[1]
						break

		elif text.lower() == 'clear':
			alist_role = getFile(ro_alist,[])
			tmp_role = []
			for tmp in alist_role:
				if tmp[0] != jid:
					tmp_role.append(tmp)
			writefile(ro_alist,str(tmp_role))
			msg = u'Очищено для '+str(jid)

		else:
			who = text.split('\n',2)[0]
			try:
				ttime = text.split('\n',2)[1]
				tttime = int(ttime[:-1])
				tmode = ttime[-1:].lower()
				tkpd = {'s':1, 'm':60, 'h':3600, 'd':86400}
				tttime = tttime*tkpd[tmode]
			except:
				tttime = 0
				try:
					reason = text.split('\n',2)[1]
				except:
					reason = u'No reason!'
			if tttime:
				try:
					reason = text.split('\n',2)[2]
				except:
					reason = u'No reason!'
			mdb = sqlite3.connect(agestatbase)
			cu = mdb.cursor()
			fnd = cu.execute('select nick,jid from age where room=? and (nick=? or jid=?)',(jid,who,who)).fetchall()
			if len(fnd) == 1:
				whonick = unicode(fnd[0][0])
				whojid = unicode(fnd[0][1])
				skip = 0
			elif len(fnd) > 1:
				msg = u'Я видела несколько человек с таким ником. Укажите точнее!'
			else:
				msg = u'Я не в курсе кто такой '+who
	else:
		msg = u'Ась?'
	
	if skip:
		send_msg(type, jid, nick, msg)
	else:
		alist_role = getFile(ro_alist,[])
		for tmp in alist_role:
			if tmp[0] == jid and tmp[2] == whojid:
				alist_role.remove(tmp)
		if tttime:
			alist_role.append((jid,nick,whojid,role,reason,tttime+int(time.time())))
		else:
			alist_role.append((jid,nick,whojid,role,reason,0))
		iqid = str(randint(1,100000))
		i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':role, 'nick':unicode(whonick)},[Node('reason',{},reason)])])])
		cl.send(i)
		writefile(ro_alist,str(alist_role))
		send_msg(type, jid, nick, 'done')
# ----------------------------------------------

# room, jid, time

def check_unban():
	unban_log = getFile(tban,[])
	if unban_log != '[]':
		ubl = []
		for ub in unban_log:
			if ub[2] > int(time.time()):
				ubl.append(ub)
			else:
				iqid = str(randint(1,100000))
				i = Node('iq', {'id': iqid, 'type': 'set', 'to':ub[0]}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'none', 'jid':getRoom(unicode(ub[1]))},[])])])
				cl.send(i)
		if unban_log != ubl:
			writefile(tban,str(ubl))

def decrease_alist_role():
	alist_role = getFile(ro_alist,[])
	if alist_role != []:
		tmp_role = []
		for tmp in alist_role:
			if tmp[5] == 0 or tmp[5] > int(time.time()):
				tmp_role.append(tmp)
		if alist_role != tmp_role:
			writefile(ro_alist,str(tmp_role))

# ----------------------------------------------
def muc_afind(type, jid, nick, text):
	skip = 1
	if len(text):
			who = text
			mdb = sqlite3.connect(agestatbase)
			cu = mdb.cursor()
			fnd = cu.execute('select nick,jid from age where room=? and (nick=? or jid=?)',(jid,who,who)).fetchall()
			if len(fnd) == 1:
				whonick = unicode(fnd[0][0])
				whojid = unicode(fnd[0][1])
				skip = 0
			elif len(fnd) > 1:
				msg = u'Я видела несколько человек с таким ником. Укажите точнее!'
			else:
				msg = u'Я не в курсе кто такой '+who
	else:
		msg = u'Ась?'
	
	if not skip:
		alist_role = getFile(ro_alist,[])
		not_found = 1
		for tmp in alist_role:
			if tmp[0] == jid and tmp[2] == whojid:
				msg = u'Найдено в списке: '+tmp[3]+' ('+tmp[2]+u'), причина: '+tmp[4]+' (by '+tmp[1]+')'
				if tmp[5]:
					msg += ' '+un_unix(tmp[5]-int(time.time()))
				not_found = 0
				break
		if not_found:
			msg = text + u' в alist не найдено.'
	send_msg(type, jid, nick, msg)

# ----------------------------------------------
#room,jid,nick,type,text

def alist_role_presence(room,jid,nick,type,text):
#	print 'presence:',room,jid,nick,type,text
	alist_role = getFile(ro_alist,[])
	if alist_role != []:
		for tmp in alist_role:
			if tmp[0] == room and tmp[2] == jid:
				iqid = str(randint(1,100000))
				i = Node('iq', {'id': iqid, 'type': 'set', 'to':tmp[0]}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':tmp[3], 'nick':unicode(nick)},[Node('reason',{},tmp[4])])])])
				cl.send(i)

#def alist_message(room,jid,nick,type,text):
#	print 'message:',room,jid,nick,type,text

# ----------------------------------------------

global execute, timer, presence_control#, message_control

timer = [check_unban,decrease_alist_role]
presence_control = [alist_role_presence]
#message_control = [alist_message]

execute = [(1, u'ban', muc_ban, 2, u'Забанить участника'),
	   (1, u'tban', muc_tempo_ban, 2, u'Временный бан.\ntban show|del [jid] - показать/удалить временные баны\ntban nick\ntimeD|H|M|S\nreason - бан ника nick на срок time по причине reason'),
	   (1, u'none', muc_none, 2, u'Удаление аффиляции'),
	   (1, u'member', muc_member, 2, u'Сделать участника постоянным'),
#	   (1, u'admin', muc_admin, 2, u''),
#	   (1, u'owner', muc_owner, 2, u''),
	   (1, u'afind', muc_afind, 2, u'Поиск учстника в alist.'),
	   (1, u'kick', muc_kick, 2, u'Выгнать участника'),
	   (1, u'participant', muc_participant, 2, u'Сделать участника без полномочий'),
	   (1, u'visitor', muc_visitor, 2, u'Сделать участника гостем'),
	   (1, u'moderator', muc_moderator, 2, u'Сделать учасника модератором'),
	   (1, u'akick', muc_akick, 2, u'Автокик.\nakick show|del [jid] - показать/удалить автокик\nakick nick\ntimeD|H|M|S\nreason - автоматически выгонять ник nick на срок time по причине reason'),
	   (1, u'aparticipant', muc_aparticipant, 2, u'Автоучастник.\naparticipant show|del [jid] - показать/удалить автоучастник\naparticipant nick\ntimeD|H|M|S\nreason - автоматически делать ник nick участником на срок time по причине reason'),
	   (1, u'avisitor', muc_avisitor, 2, u'Автогость.\navisitor show|del [jid] - показать/удалить автогостя\navisitor nick\ntimeD|H|M|S\nreason - автоматически делать ник nick гостем на срок time по причине reason'),
	   (1, u'amoderator', muc_amoderator, 2, u'Автомодератор.\namoderator show|del [jid] - показать/удалить автомодератор\namoderator nick\ntimeD|H|M|S\nreason - автоматически делать ник nick модератором на срок time по причине reason')]
