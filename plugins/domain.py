#!/usr/bin/python
# -*- coding: utf-8 -*-

def domaininfo(type, jid, nick, text):
	if text.lower().count('sites'): t, text, regex, msg = 2, text.split(' ')[1], '<font color="black" size="2">(.*?)</font>', L('Sites at Domain/IP address: %s\n') % text.split(' ')[1]
	else: t, regex, msg = 1, '<blockquote>(.*?)</blockquote>', L('Domain/IP address info:')
	url = 'http://1whois.ru/index.php?url=%s&t=%s' % (text,t)
	body = html_encode(urllib.urlopen(url).read().replace('&nbsp;', ' '))
	body = re.findall(regex, body, re.S)[0]
	if body.count(u'Нет данных!'): msg += ' '+ L('No data!')
	else: msg += '\n'+replacer(body)
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, 'domain_info', domaininfo, 2, L('Domain/IP address whois info.'))]