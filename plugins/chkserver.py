#!/usr/bin/python
# -*- coding: utf-8 -*-


def chkserver(type, jid, nick, text):
	if text.count('.') and text.count(':') and len(text) > 5:
		url = u'http://status.blackout-gaming.net/status.php?dns='+text.replace(':','&port=')+u'&style=t1'
		body = urllib.urlopen(url).read()
		body = (body.split('("')[1])[:-3]
		msg = u'Статус сервера: '+ body
	else: msg = u'Что будем проверять?'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'chkserver', chkserver, 2, u'Проверка активности сервиса на запрашиваемом сервере:\n chkserver server:port')]