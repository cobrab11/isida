#!/usr/bin/python
# -*- coding: utf -*-

# by ferym@jabbim.org.ru

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
				send_msg(type, jid, nick, L('Send for you in private'))
				send_msg('chat', jid, nick, message)
				return
		else:
			send_msg(type, jid, nick, message)
	except:
		send_msg(type, jid, nick, L('Something broked.'))

global execute

execute = [(0, 'anek', anek, 1, L('Show random	anecdote | Author: ferym'))]
