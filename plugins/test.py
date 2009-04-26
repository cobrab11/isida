#!/usr/bin/python
# -*- coding: utf -*-

def test(type, jid, nick):
	send_msg(type, jid, nick, 'passed')

def test_rus(type, jid, nick):
	send_msg(type, jid, nick, u'две полоски!')

#------------------------------------------------

# в начале
# 0 - всем
# 1 - админам\овнерам
# 2 - владельцу бота

# в конце
# 0 - передавать параметры
# 1 - ничего не передавать
# 2 - передавать остаток текста

global execute

execute = [(0, prefix+u'test', test, 1),
           (0, prefix+u'тест', test_rus, 1)]
