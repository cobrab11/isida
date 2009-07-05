#!/usr/bin/python
# -*- coding: utf -*-

def sys_shell(type, jid, nick, text, mode):
	if os.path.isfile('tmp'):
		os.system('rm -r tmp')
	a = os.system(text+' > tmp')
	if a:
		msg = u'Ошибка выполнения команды!'
	else:
		try:
			msg = readfile('tmp').decode('utf-8')
			if mode:
				msg = 'done'
		except:
			msg = u'Ошибка получения результата!'
	send_msg(type, jid, nick, msg)

def shell(type, jid, nick, text):
	sys_shell(type, jid, nick, text, 0)

def shell_silent(type, jid, nick, text):
	sys_shell(type, jid, nick, text, 1)

global execute, timer, sys_shell

timer = []

execute = [(2, u'sh', shell, 2),
	   (2, u'sh_silent', shell_silent, 2)]
