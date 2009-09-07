#!/usr/bin/python
# -*- coding: utf -*-

def null_vars():
	return {'none/visitor':0,'none/participant':0,'none/moderator':0,'member/visitor':0,'member/participant':0,'member/moderator':0,'admin/moderator':0,'owner/moderator':0}

def gstats(type, jid, nick):
	msg = u'За последнюю сессию ('+un_unix(int(time.time())-sesstime)+u') я видела всего:'
	vars = null_vars()

	for mega in megabase2:
			ta = mega[3]+'/'+mega[2]
			for va in vars:
				if va == ta: vars[ta]+=1
	for va in vars:
		if vars[va]: msg += '\n'+str(va)+' '+str(vars[va])
	send_msg(type, jid, nick, msg)

def stats(type, jid, nick):
	msg = u'За последнюю сессию ('+un_unix(int(time.time())-sesstime)+u') я видела здесь:'
	vars = null_vars()

	for mega in megabase2:
		if mega[0] == jid:
			ta = mega[3]+'/'+mega[2]
			for va in vars:
				if va == ta: vars[ta]+=1
	for va in vars:
		if vars[va]: msg += '\n'+str(va)+' '+str(vars[va])
	send_msg(type, jid, nick, msg)

global execute

execute = [(1, u'stat', stats, 1, u'Локальная статистика посещений конференции'),
	 (1, u'gstat', gstats, 1, u'Глобальная статистика посещений конференций')]
