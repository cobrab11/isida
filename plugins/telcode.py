#!/usr/bin/python
# -*- coding: utf -*-

def telcode(type, jid, nick, text):
	query = urllib.urlencode({'text' : text.encode("windows-1251")})
	url = u'http://www.telcode.ru/mob/select.asp?%s'.encode("utf-8") % (query)
	f = urllib.urlopen(url)
	body = f.read()
	f.close()
	body = html_encode(body)
	if body.count(u'Не найдено записей'): msg = u'Не найдено!'
	else:
		msg = rss_del_html(get_tag(body,'h3'))+' ... '
		city = body.replace('\n','').replace('\r','').split('</h3>')[1].split('<br> <br>')[0].split('<br>')
		for tmp in city: msg += get_tag(tmp,'a')+', '
		msg = msg[:-2]
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'telcode', telcode, 2, u'Определение кода города')]
