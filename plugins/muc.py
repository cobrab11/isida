#!/usr/bin/python
# -*- coding: utf -*-

# -------------- affiliation -----------------

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

global execute

execute = [(1, u'ban', muc_ban, 2),
	   (1, u'none', muc_none, 2),
	   (1, u'member', muc_member, 2),
	   (1, u'admin', muc_admin, 2),
	   (1, u'owner', muc_owner, 2),
	   (1, u'kick', muc_kick, 2),
	   (1, u'participant', muc_participant, 2),
	   (1, u'visitor', muc_visitor, 2),
	   (1, u'moderator', muc_moderator, 2)]
