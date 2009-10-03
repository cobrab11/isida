#!/usr/bin/python
# -*- coding: utf-8 -*-

# written by dr.Schmurge
# fixed by Disabler

time_limit_base = set_folder+u'saytoowner.db'
amsg_limit = [86400,3600,60] # лимит размера сообщения

def adminmail(type, jid, nick, text):
	if len(text):
		if len(text) > amsg_limit: text = text[:amsg_limit]+'[...]'
       		timesent = getFile(time_limit_base, {})
       		ga = get_access(jid, nick)
		fjid = getRoom(ga[1])
		tmp_lim = amsg_limit[ga[0]]
		if timesent.has_key(fjid):
                        wt = int(timesent[fjid]-time.time())
                        if wt >= 0:
                                send_msg(type, jid, nick, u'Превышен лимит скорости посылки сообщений. Подождите: '+un_unix(wt))
                                return None
                        else: del timesent[fjid]
		timesent[fjid] = int(time.time())+tmp_lim
		writefile(time_limit_base, str(timesent))
		msg = u'Пользователь '+nick+u' ['+fjid+u'] из комнаты '+jid+u' в '+str(time.strftime("%H:%M", time.localtime (time.time())))+u' отправил вам сообщение: '+text
		for ajid in ownerbase: send_msg('chat', getRoom(ajid), '', msg)
		send_msg(type, jid, nick, u'Отправила')
	else: send_msg(type, jid, nick, u'Что-то отправить хочешь?')

global execute

execute = [(0, u'msgtoadmin', adminmail, 2, u'Отправить сообщение владельцу бота.\nmsgtoadmin текст сообщения')]
