#!/usr/bin/python
# -*- coding: utf-8 -*-

blacklist_base = set_folder + u'blacklist.db'

def check_blacklist(room):
	lst = getFile(blacklist_base, [])
	try:
		lst.index(room)
		return True
	except: return False

def blacklist(type, jid, nick, text): 
	text, msg = unicode(text), u''
	templist = getFile(blacklist_base, [])
	text = text.split(' ')
	if text[0] == 'add':
		if text[1] in templist: msg = u'Конференция уже находится в черном списке.'
		else:
			templist.append(text[1])
			msg = u'Добавлено: '+text[1]
	elif text[0] == 'del':
		if text[1] in templist: msg = u'Удалена: '+str(templist.pop(templist.index(text[1])))
		else: msg = u'Конференция отсутствует в списке.'
	elif text[0] == 'show':
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

execute = [(2, u'blacklist', blacklist, 2, u'Черный список конференций.\nblacklist add|del|show|clear')]