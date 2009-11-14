#!/usr/bin/python
# -*- coding: utf-8 -*-

blacklist_base = set_folder + u'blacklist.db'

def leave_room(rjid, reason):
	global confbase, confs
	msg = u''
	for i in range(0, len(confbase)):
		if rjid == getRoom(confbase[i]):
			confbase.remove(confbase[i])
			writefile(confs, str(confbase))
			leaveconf(rjid, domain, reason)
			msg = u'Свалила из '+ rjid + '\n'
	return msg

def blacklist(type, jid, nick, text): 
	global confbase, lastserver
	text, msg = unicode(text.lower()), u''
	templist = getFile(blacklist_base, [])
	reason = u'Конференция занесена в черный список'
	try:
		text = text.split(' ')
		if not text[1].count('@'): text[1] += '@'+lastserver
		if text[0] == 'add':
			if text[1] in templist: msg = u'Адрес уже содержится в списке.'
			elif len(confbase)==1 and text[1] == getRoom(confbase[0]):
				msg =u'Нельзя добавлять последнюю конференцию в черный список'
			else:
				msg = leave_room(text[1], reason)
				templist.append(text[1])
				msg += u'Добавлено в черный список: '+str(text[1])
		elif text[0] == 'del':
			if text[1] in templist: msg = u'Удалено из черного списка: '+str(templist.pop(templist.index(text[1])))
			else: msg = u'Адрес отсутствует в списке.'
		else: msg = u'Ошибка в параметрах, прочитайте помощь по команде.'
	except:
		if text[0] == 'show':
			if len(templist) == 0: msg = u'Список пуст'
			else:
				msg, n = u'Список конференций:\n', 1
				for i in range(0, len(templist)):
					msg += str(n)+'. '+templist[i]+'\n'
					n += 1
				msg = msg[:-1]
		elif text[0] == 'clear': msg, templist = u'Очищено.', []
		else: msg = u'Ошибка в параметрах, прочитайте помощь по команде.'
	writefile(blacklist_base, str(templist))
	send_msg(type, jid, nick, msg)


global execute

execute = [(2, u'blacklist', blacklist, 2, u'Черный список конференций.\nblacklist add|del|show|clear\nblacklist add|del room@conference.server.tld - добавить|удалить конферецию из черного списка\nblacklist show - показать список\nblacklist clear - очистить список')]