#!/usr/bin/python
# -*- coding: utf -*-

def test(type, jid, nick):
	send_msg(type, jid, nick, 'passed')

def test_rus(type, jid, nick):
	send_msg(type, jid, nick, u'две полоски!')

global execute

execute = [(0, u'test', test, 1, u'Проверка на "живость" бота.'),
	   (0, u'тест', test_rus, 1, u'Проверка на "живость" бота.')]
