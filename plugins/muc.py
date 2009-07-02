#!/usr/bin/python
# -*- coding: utf -*-

tban = set_folder+u'temporary.ban'		# лог временного бана

# -------------- affiliation -----------------

def muc_tempo_ban(type, jid, nick,text):
	if text[:4].lower() == 'show' and not text.count('\n'):
		text = text[5:]
		if not len(text):
			text = '.'
		ubl = getFile(tban,[])
		msg = ''
		for ub in ubl:
			if ub[0] == jid and ub[1].count(text):
				msg += u'\n'+ub[1]+u'\t'+un_unix(ub[2])
		if len(msg):
			msg = u'Найдено:'+msg
		else:
			msg = u'Не найдено!'
		send_msg(type, jid, nick, msg)
		
	else:
		muc_tempo_ban2(type, jid, nick,text)

def muc_tempo_ban2(type, jid, nick,text):
	skip = 1
	if len(text):
		who = text.split('\n',2)[0]
		ttime = text.split('\n',2)[1]
		try:
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
			mdb = sqlite3.connect(mainbase)
			cu = mdb.cursor()
			fnd = cu.execute('select jid from age where room=? and (nick=? or jid=?)',(jid,who,who)).fetchall()
			if len(fnd) == 1:
				whojid = fnd[0][0]
				skip = 0
			elif len(fnd) > 1:
				msg = u'Я видела несколько человек с таким ником. Укажите точнее!'
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
		i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'outcast', 'jid':getRoom(str(whojid))},[Node('reason',{},reason)])])])
		cl.send(i)

		ubl = getFile(tban,[])
		for ub in ubl:
			if ub[0] == jid and ub[1] == whojid:
				ubl.remove(ub)
		ubl.append((jid,whojid,tttime))
		writefile(tban,str(ubl))
		send_msg(type, jid, nick, 'done')

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
	skip = 1
	if len(text):
		if text.count('\n'):
			who = text.split('\n',1)[0]
			reason = text.split('\n',1)[1]
		else:
			who = text
			reason = u'by Isida!'

		mdb = sqlite3.connect(mainbase)
		cu = mdb.cursor()
		fnd = cu.execute('select jid from age where room=? and (nick=? or jid=?)',(jid,who,who)).fetchall()
		if len(fnd) == 1:
			whojid = fnd[0][0]
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
		iqid = str(randint(1,100000))
		i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':aff, 'jid':getRoom(str(whojid))},[Node('reason',{},reason)])])])
		cl.send(i)
		send_msg(type, jid, nick, 'done')

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

		mdb = sqlite3.connect(mainbase)
		cu = mdb.cursor()
		fnd = cu.execute('select nick from age where room=? and (nick=? or jid=?)',(jid,who,who)).fetchall()
		if len(fnd) == 1:
			whonick = fnd[0][0]
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
		iqid = str(randint(1,100000))
		i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':role, 'nick':whonick},[Node('reason',{},reason)])])])
		cl.send(i)
		send_msg(type, jid, nick, 'done')

# ----------------------------------------------
# room, jid, time

def check_unban():
	unban_log = getFile(tban,[])
	if unban_log != '[]':
		ubl = []
		for ub in unban_log:
			if ub[2]:
				ubl.append((ub[0],ub[1],ub[2]-1))
			else:
				iqid = str(randint(1,100000))
				i = Node('iq', {'id': iqid, 'type': 'set', 'to':ub[0]}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'none', 'jid':getRoom(str(ub[1]))},[])])])
				cl.send(i)
		writefile(tban,str(ubl))
	sleep(1)
	sys.exit(0)

# ----------------------------------------------

global execute, timer

timer = [check_unban]

execute = [(1, u'ban', muc_ban, 2),
	   (1, u'tban', muc_tempo_ban, 2),
	   (1, u'none', muc_none, 2),
	   (1, u'member', muc_member, 2),
	   (1, u'admin', muc_admin, 2),
	   (1, u'owner', muc_owner, 2),
	   (1, u'kick', muc_kick, 2),
	   (1, u'participant', muc_participant, 2),
	   (1, u'visitor', muc_visitor, 2),
	   (1, u'moderator', muc_moderator, 2)]
