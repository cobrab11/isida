#!/usr/bin/python
# -*- coding: utf-8 -*-

def known(type, jid, nick, text):
	text = text.strip()
	if text == '': text = nick
	mdb = sqlite3.connect(agestatbase)
	cu = mdb.cursor()
	real_jid = cu.execute('select jid from age where room=? and (nick=? or jid=?)',(jid,text,text.lower())).fetchone()
	if real_jid:
		nicks = cu.execute('select nick from age where room=? and jid=?',(jid,real_jid[0])).fetchall()
		if text == nick: msg = L('I know you as: ')
		else: msg = L('I know %s as: ') % text
		for tmp in nicks:
			msg += tmp[0] + ', '
		msg = msg[:-2]
	else: msg = L('Not found!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, 'known', known, 2, L('Show user\'s nick changes.'))]
