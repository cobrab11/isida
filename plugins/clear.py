#!/usr/bin/python
# -*- coding: utf -*-

def hidden_clear(type, jid, nick, text):
	try: cntr = int(text)
	except: cntr = 20
	if cntr < 1 or cntr > 100: cntr = 20
	pprint(u'clear: '+unicode(jid)+u' by: '+unicode(nick))
	send_msg(type, jid, nick, u'Начинаю зачистку! Сообщений: '+str(cntr)+u', время зачистки примерно '+str(int(cntr*1.3))+u' сек.')
	while (cntr>0):
		cl.send(xmpp.Message(jid, '', "groupchat"))
		time.sleep(1.3)
		cntr=cntr-1
	send_msg(type, jid, nick, u'стерильно!!!')

global execute

execute = [(1, u'clear', hidden_clear, 2, u'Скрытая очистка истории сообщений. По умолчанию будет послано 20 скрытых + 1 сообщение в конференцию. Можно задать свой параметр от 2 до 100.')]
