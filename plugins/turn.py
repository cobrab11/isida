#!/usr/bin/python
# -*- coding: utf -*-

turn_base = []

def turner(type, jid, nick, text):
	global turn_base
	rtab = u'йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁqwertyuiop[]asdfghjkl;\'zxcvbnm,.`QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>~'
	ltab = u'qwertyuiop[]asdfghjkl;\'zxcvbnm,.`QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>~йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ'
	for tmp in turn_base:
		if tmp[0] == jid and tmp[1] == nick:
			turn_base.remove(tmp)
			msg = ''
			for tex in tmp[2]:
				notur = 1
				for i in range(0,len(rtab)):
					if tex == rtab[i]:
						msg += ltab[i]
						notur = 0
						break
				if notur: msg += tex
			gl_censor = getFile(cns,[(getRoom(jid),0)])
			if int((getRoom(jid),1) in gl_censor):
				msg = to_censore(msg)
			send_msg(type, jid, nick, msg)
			break

def append_to_turner(room,jid,nick,type,text):
	global turn_base
	for tmp in turn_base:
		if tmp[0] == room and tmp[1] == nick:
			turn_base.remove(tmp)
			break
	turn_base.append((room,nick,text))
	sys.exit(0)

def remove_from_turner(room,jid,nick,type,text):
	global turn_base
	if type=='unavailable':
		for tmp in turn_base:
			if tmp[0] == room and tmp[1] == nick:
				turn_base.remove(tmp)
				break
	sys.exit(0)

global execute

message_control = [append_to_turner]
presence_control = [remove_from_turner]

execute = [(0, u'turn', turner, 2, u'"Перевернуть" последнее сообщение с русского на английский и обратно.')]
