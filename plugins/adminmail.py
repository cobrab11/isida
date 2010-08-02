#!/usr/bin/python
# -*- coding: utf-8 -*-

# written by dr.Schmurge
# fixed by Disabler

def adminmail(type, jid, nick, text):
	if len(text):
		if len(text) > GT('amsg_limit_size'): text = text[:GT('amsg_limit_size')]+u'[…]'
		timesent = getFile(time_limit_base, {})
		ga = get_level(jid, nick)
		fjid = getRoom(ga[1])
		tmp_lim = GT('amsg_limit')[ga[0]]
		if timesent.has_key(fjid):
			wt = int(timesent[fjid]-time.time())
			if wt >= 0:
				send_msg(type, jid, nick, L('Time limit exceeded. Wait: %s') % un_unix(wt))
				return None
			else: del timesent[fjid]
		timesent[fjid] = int(time.time())+tmp_lim
		writefile(time_limit_base, str(timesent))
		msg = L('User %s (%s) from %s at %s send massage to you: %s') % (nick,fjid,jid,str(time.strftime("%H:%M %d.%m.%y", time.localtime (time.time()))),text)
		for ajid in ownerbase: send_msg('chat', getRoom(ajid), '', msg)
		send_msg(type, jid, nick, L('Sent'))
	else: send_msg(type, jid, nick, L('What?'))

global execute

execute = [(4, 'msgtoadmin', adminmail, 2, L('Send message to bot\'s owner\nmsgtoadmin text'))]
