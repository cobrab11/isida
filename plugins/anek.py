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
		message = rss_replace(unicode(message,'windows-1251'))
		if type=='groupchat':
			if len(message)<500:
				send_msg(type, jid, nick, message)
			else:
				send_msg(type, jid, nick, u'Отправила в приват')
				send_msg('chat', jid, nick, message)
				return
		else:
			send_msg(type, jid, nick, message)
	except:
		send_msg(type, jid, nick, u'что-то сломалось')

global execute

execute = [(0, u'anek', anek, 1, u'Показывает случайный анекдот с интернет ресурса | author ferym')]
