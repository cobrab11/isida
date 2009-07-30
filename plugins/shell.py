#!/usr/bin/python
# -*- coding: utf -*-

def shell(type, jid, nick, text):
	sysshell(type, jid, nick, text, 1)

def shell_silent(type, jid, nick, text):
	sysshell(type, jid, nick, text, 0)

def sysshell(type, jid, nick, text, mode):
	try:
		sh_ex = "bash -c '%s' 2>&1"%(text.replace("'","'\\''"))
		p = os.popen(sh_ex)
		msg = p.read().decode('utf8', 'replace')
	except: msg = u'Произошла ошибка обработки команды'
	if mode: send_msg(type, jid, nick, msg)

global execute

execute = [(2, u'sh', shell, 2, u'Выполнение shell команды.'),
	   (2, u'sh_silent', shell_silent, 2, u'Выполнение shell команды без показа вывода команды.')]
