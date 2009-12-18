#!/usr/bin/python
# -*- coding: utf -*-

clear_delay = 1.3

def hidden_clear(type, jid, nick, text):
	try: cntr = int(text)
	except: cntr = 20
	if cntr < 1 or cntr > 100: cntr = 20
	pprint(u'clear: '+unicode(jid)+u' by: '+unicode(nick))
	send_msg(type, jid, nick, u'Начинаю зачистку! Сообщений: '+str(cntr)+u', время зачистки примерно '+str(int(cntr*clear_delay))+u' сек.')
	time.sleep(clear_delay)
	for tmp in range(0,cntr):
		cl.send(xmpp.Message(jid, '', "groupchat"))
		time.sleep(clear_delay)
	send_msg(type, jid, nick, u'стерильно!!!')

global execute

execute = [(1, u'clear', hidden_clear, 2, u'Скрытая очистка истории сообщений. По умолчанию будет послано 20 скрытых + 1 сообщение в конференцию. Можно задать свой параметр от 2 до 100.')]
