#!/usr/bin/python
# -*- coding: utf -*-

hide_conf = set_folder+'hidenroom.db'

def hide_room(type, jid, nick, text):
	if type == 'groupchat': msg = L('This command aviable only in private!')
	else:
		hmode = text.split(' ')[0]
		try: hroom = text.split(' ')[1]
		except: hroom = jid
		hr = getFile(hide_conf,[])
		if hmode == 'show':
			if len(hr):
				msg = L('Hidden conferences:')
				for tmp in hr: msg += '\n'+tmp
			else: msg = L('No hidden conferences.')
		elif hmode == 'add':
			if not match_room(hroom): msg = L('I am not in the %s') % hroom
			elif hr.count(hroom): msg = L('I\'m already hide a %s') % hroom
			else:
				hr.append(hroom)
				msg = L('%s has been hidden') % hroom
				writefile(hide_conf,str(hr))
		elif hmode == 'del':
			if not match_room(hroom): msg = L('I am not in the %s') % hroom
			elif hr.count(hroom):
				hr.remove(hroom)
				msg = L('%s will be shown') % hroom
				writefile(hide_conf,str(hr))
		else: msg = L('What?')
	send_msg(type, jid, nick, msg)

global execute

execute = [(2, 'hide', hide_room, 2, L('Hide conference.\nhide [add|del|show] [room@conference.server.tld]'))]
