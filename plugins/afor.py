#!/usr/bin/python
# -*- coding: utf -*-

# by ferym@jabbim.org.ru

def afor(type, jid, nick):
	try:
		target = urllib2.urlopen('http://skio.ru/quotes/humour_quotes.php').read()
		od = re.search('<form id="qForm" method="post"><div align="center">',target)
		message = target[od.end():]
		message = message[:re.search('</div>',message).start()]
		msg = rss_replace(unicode(message.strip(),'windows-1251'))
	except: msg = L('Something broked.')
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, 'afor', afor, 1, L('Show random aphorism from skio.ru | Author: ferym'))]
