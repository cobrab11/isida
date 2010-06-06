#!/usr/bin/python
# -*- coding: utf -*-

def private_paste(type, jid, nick, text):
	if type == 'groupchat': msg = L('This command available only in private!')
	else: msg = paste_text(text,jid,get_level(jid,nick)[1])
	send_msg(type, jid, nick, msg)
	
def public_paste(type, jid, nick, text):
	if type == 'groupchat': msg = L('This command available only in private!')
	else: msg,type,nick = L('%s pasted by %s') % (paste_text(text,jid,get_level(jid,nick)[1]),nick),'groupchat',''
	send_msg(type, jid, nick, msg)
	
global execute

execute = [(4, 'paste', public_paste, 2, L('Paste some text to server')),
		   (5, 'ppaste', private_paste, 2, L('Paste some text to server'))]
