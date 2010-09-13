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

if not GT('paranoia_mode'): execute = [(9, 'sh', shell, 2, L('Execute shell command.')),
	   (9, 'sh_silent', shell_silent, 2, L('Execute shell command without output result.'))]
