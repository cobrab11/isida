#!/usr/bin/python
# -*- coding: utf -*-

def bot_shutdown(type, jid, nick, text, reason, xtype):
	global game_over,bot_exit_type
	StatusMessage = L('%s by command from %s') % (reason, nick)
	if text != '': StatusMessage += ', ' + L('reason: %s') % text
	send_presence_all(StatusMessage)
	bot_exit_type, game_over = xtype, True

def bot_exit(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, L('Shutdown'), 'exit')

def bot_restart(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, L('Restart'), 'restart')

def bot_update(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, L('Autoupdate'), 'update')

global execute

execute = [(9, 'quit', bot_exit, 2, L('Shutting down the bot. You can set reason.')),
	 (9, 'restart', bot_restart, 2, L('Restart the bot. You can set reason.')),
	 (9, 'update', bot_update, 2, L('Autoupdate from SVN. You can set reason.'))]
