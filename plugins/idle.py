#!/usr/bin/python
# -*- coding: utf -*-

idle_base = []

def idle(type, jid, nick, text):
	global idle_base
	if not len(text): text = nick
	msg = u'Не могу найти '+text
	for tmp in idle_base:
		if tmp[0] == jid and tmp[1] == text:
			if text == nick: msg = u'Последняя твоя активность'
			else: msg = u'Последняя активность '+text
			msg += u' была '+un_unix(int(time.time())-tmp[3])+u' назад ('
			if tmp[2] == 'm': msg += u'сообщение)'
			else: msg += u'презенс)'
			break
	send_msg(type, jid, nick, msg)

def append_to_idle(room,jid,nick,type,text):
	global idle_base
	for tmp in idle_base:
		if tmp[0] == room and tmp[1] == nick:
			idle_base.remove(tmp)
			break
	idle_base.append((room,nick,'m',int(time.time())))
	sys.exit(0)

def remove_from_idle(room,jid,nick,type,text):
	global idle_base
	for tmp in idle_base:
		if tmp[0] == room and tmp[1] == nick:
			idle_base.remove(tmp)
			break
	if type!='unavailable':
		idle_base.append((room,nick,'p',int(time.time())))
	sys.exit(0)

global execute

message_control = [append_to_idle]
presence_control = [remove_from_idle]

execute = [(0, u'idle', idle, 2, u'Время с момента последней активности')]
