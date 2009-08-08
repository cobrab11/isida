#!/usr/bin/python
# -*- coding: utf -*-

def say(type, jid, nick, text):
	send_msg('groupchat', jid, '', to_censore(text))	

def gsay(type, jid, nick, text):
	for jjid in confbase: send_msg('groupchat', getRoom(jjid), '', text)

global execute

execute = [(1, u'say', say, 2, u'Команда "Сказать". Бот выдаст в текущую конференцию всё, что будет после команды say.'),
	 (2, u'gsay', gsay, 2, u'Глобальное объявление во всех конференциях, где находится бот.')]
