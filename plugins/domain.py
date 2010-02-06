#!/usr/bin/python
# -*- coding: utf-8 -*-

def domaininfo(type, jid, nick, text):
	if text.count('sites'): t, text, spl, msg = 2, text.split(' ')[1], '<font color="black" size="2">', L('Sites at Domain/IP address: %s\n') % text.split(' ')[1]
	else: t, spl, msg = 1, '<blockquote>', L('Domain/IP address info:')
	url = u'http://1whois.ru/index.php?url='+str(text)+u'&t='+str(t)
	body = html_encode(urllib.urlopen(url).read().replace('&nbsp;', ' '))
	body = body.split(spl)[1].split('Generation time:')[0]
	if body.count(u'Нет данных!'): msg += ' '+ L('No data!')
	else: msg += '\n'+replacer(body)
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'domain_info', domaininfo, 2, L('Domain/IP address whois info.'))]