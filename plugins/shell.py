#!/usr/bin/python
# -*- coding: utf -*-

def shell(type, jid, nick, text):
	sysshell(type, jid, nick, text, 1)

def shell_silent(type, jid, nick, text):
	sysshell(type, jid, nick, text, 0)

def sysshell(type, jid, nick, text, mode):
	try:
		cmd = "bash -c '%s' 2>&1"%(text.replace("'","'\\''"))
		p = popen2.Popen3(cmd, True)
		while p.poll() == -1: pass
		msg = concat(p.fromchild.readlines()).decode('utf-8')
	except: msg = u'Произошла ошибка обработки команды'
	if mode: send_msg(type, jid, nick, msg)

global execute

execute = [(2, u'sh', shell, 2, u'Выполнение shell команды.'),
	   (2, u'sh_silent', shell_silent, 2, u'Выполнение shell команды без показа вывода команды.')]
