#!/usr/bin/python
# -*- coding: utf -*-

def shell(type, jid, nick, text):
	sysshell(type, jid, nick, text, 1)

def shell_silent(type, jid, nick, text):
	sysshell(type, jid, nick, text, 0)

def sysshell(type, jid, nick, text, mode):
	msg = shell_execute(text)
	if mode: send_msg(type, jid, nick, msg)

global execute

execute = [(2, u'sh', shell, 2, u'Выполнение shell команды.'),
	   (2, u'sh_silent', shell_silent, 2, u'Выполнение shell команды без показа вывода команды.')]
