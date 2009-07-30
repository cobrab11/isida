#!/usr/bin/python
# -*- coding: utf -*-

# by ferym@jabbim.org.ru

import urllib2


def anek(type, jid, nick):
	try:
		req = 'http://anekdot.odessa.ua/rand-anekdot.php'
		r = urllib2.urlopen(req)
		target = r.read()
		od = re.search('background-color:#FFFFFF\'>',target)
		message = target[od.end():]
		message = message[:re.search('<br>',message).start()]
		message = message.replace('<br />','')
		message = message.strip()
		if type=='groupchat':
			if len(message)<500:
				send_msg(type, jid, nick, unicode(message,'windows-1251'))
			else:
				send_msg(type, jid, nick, u'Отплавила в приват')
				send_msg('chat', jid, nick, unicode(message,'windows-1251'))
				return
		else:
			send_msg(type, jid, nick, unicode(message,'windows-1251'))
	except:
		send_msg(type, jid, nick, u'что-то сломалось')
    
    
global execute


execute = [(0, u'anek', anek, 1, u'показывает случайный анекдот с интернет ресурса | author ferym')]
