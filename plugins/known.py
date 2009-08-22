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
		if text == nick: msg = u'Я видела тебя как: '
		else: msg = u'Я видела '+text+u' как: '
		for tmp in nicks:
			msg += tmp[0] + u', '
		msg = msg[:-2]
	else: msg = u'Не найдено!'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'known', known, 2, u'Показ смены ников')]
