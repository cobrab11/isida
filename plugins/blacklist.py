#!/usr/bin/python
# -*- coding: utf-8 -*-

def leave_room(rjid, reason):
	global confbase, confs
	msg = ''
	for i in range(0, len(confbase)):
		if rjid == getRoom(confbase[i]):
			confbase.remove(confbase[i])
			writefile(confs, str(confbase))
			leaveconf(rjid, domain, reason)
			msg = L('Leave conference %s\n') % rjid
	return msg

def blacklist(type, jid, nick, text): 
	global confbase, lastserver
	text, msg = unicode(text.lower()), ''
	templist = getFile(blacklist_base, [])
	reason = L('Conference was added in blacklist')
	try:
		text = text.split(' ')
		if not text[1].count('@'): text[1] += '@'+lastserver
		if text[0] == 'add':
			if text[1] in templist: msg = L('This conference already exist in blacklist.')
			elif len(confbase)==1 and text[1] == getRoom(confbase[0]):
				msg =L('You can\'t add last conference in blacklist.')
			else:
				msg = leave_room(text[1], reason)
				templist.append(text[1])
				msg += L('Add to blacklist: %s') % str(text[1])
		elif text[0] == 'del':
			if text[1] in templist: msg = L('Removed from blacklist: %s') % str(templist.pop(templist.index(text[1])))
			else: msg = L('Address not in blacklist.')
		else: msg = L('Error in parameters. Read the help about command.')
	except:
		if text[0] == 'show':
			if len(templist) == 0: msg = L('List is empty.')
			else:
				msg, n = L('List of conferences:\n'), 1
				for i in range(0, len(templist)):
					msg += str(n)+'. '+templist[i]+'\n'
					n += 1
				msg = msg[:-1]
		elif text[0] == 'clear': msg, templist = L('Cleared.'), []
		else: msg = L('Error in parameters. Read the help about command.')
	writefile(blacklist_base, str(templist))
	send_msg(type, jid, nick, msg)

global execute

execute = [(2, 'blacklist', blacklist, 2, L('Manage of conferences blacklist.\nblacklist add|del|show|clear\nblacklist add|del room@conference.server.tld - add|remove address from blacklist\nblacklist show - show blacklist\nblacklist clear - clear blacklist'))]