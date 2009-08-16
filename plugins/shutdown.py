#!/usr/bin/python
# -*- coding: utf -*-

def bot_shutdown(type, jid, nick, text, reason, xtype):
	global game_over
	StatusMessage = reason + u' по команде от '+nick
	if text != '': StatusMessage += u', причина: '+text
	send_presence_all(StatusMessage)
	writefile(tmpf,str(xtype))
	game_over = 1

def bot_exit(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, u'Завершение работы', 'exit')

def bot_restart(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, u'Перезапуск', 'restart')

def bot_update(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, u'Самообновление', 'update')

global execute

execute = [(2, u'quit', bot_exit, 2, u'Завершение работы бота. Можно указать параметр, который будет показан в статусе бота при выходе.'),
	 (2, u'restart', bot_restart, 2, u'Перезапуск бота. Можно указать параметр, который будет показан в статусе бота при перезапуске.'),
	 (2, u'update', bot_update, 2, u'Самообновление бота из SVN.')]
