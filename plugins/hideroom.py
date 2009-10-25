#!/usr/bin/python
# -*- coding: utf -*-

hide_conf = set_folder+u'hidenroom.db'

def hide_room(type, jid, nick, text):
	if type == 'groupchat': msg = u'Команда доступна только в привате!'
	else:
		hmode = text.split(' ')[0]
		try: hroom = text.split(' ')[1]
		except: hroom = jid
		hr = getFile(hide_conf,[])
		if hmode == u'show':
			if len(hr):
				msg = u'Я скрываю конфы:'
				for tmp in hr: msg += '\n'+tmp
			else: msg = u'Скрытых конф нет.'
		elif hmode == u'add':
			if not match_room(hroom): msg = u'Меня нет в конфе '+hroom
			elif hr.count(hroom): msg = u'Я уже скрываю конфу '+hroom
			else:
				hr.append(hroom)
				msg = u'Конференция '+hroom+u' скрыта.'
				writefile(hide_conf,str(hr))
		elif hmode == u'del':
			if not match_room(hroom): msg = u'Меня нет в конфе '+hroom
			elif hr.count(hroom):
				hr.remove(hroom)
				msg = u'Конференция '+hroom+u' будет показана.'
				writefile(hide_conf,str(hr))
		else: msg = u'Что сделать?'
	send_msg(type, jid, nick, msg)

global execute

execute = [(2, u'hide', hide_room, 2, u'Скрыть конференцию.\nhide [add|del|show][ room@conference.server.tld]')]
