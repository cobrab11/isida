#!/usr/bin/python
# -*- coding: utf -*-

def get_tld(type, jid, nick, text):
	if len(text) >= 2:
		tld = readfile('tld/tld.list').decode('utf-8')
		tld = tld.split('\n')
		msg = u'Не найдено!'
		for tl in tld:
			if tl.split('\t')[0]==text:
				msg = '.'+tl.replace('\t',' - ',1).replace('\t','\n')
				break
	else:
		msg = u'Что искать то будем?'
	send_msg(type, jid, nick, msg)

def get_dns(type, jid, nick, text):
	is_ip = 0
	if text.count('.') == 3:
		is_ip = 1
		for ii in text:
			if not nmbrs.count(ii):
				is_ip = 0
				break
	if is_ip:
		try:
			msg = socket.gethostbyaddr(text)[0]

		except:
			msg = u'Не резолвится'
	else:
		try:
			ans = socket.gethostbyname_ex(text)[2]
			msg = text+' - '
			for an in ans:
				msg += an + ' | '
			msg = msg[:-2]
		except:
			msg = u'Не резолвится'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'dns', get_dns, 2, u'dns резолвер'),
	 (0, u'tld', get_tld, 2, u'Поиск доменных зон TLD')]
