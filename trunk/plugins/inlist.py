#!/usr/bin/python
# -*- coding: utf-8 -*-

def inban(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'outcast', L('Total banned: %s'))
def inowner(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'owner', L('Total owners: %s'))
def inadmin(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'admin', L('Total admins: %s'))
def inmember(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'member', L('Total members: %s'))
	
def inlist_raw(type, jid, nick, text, affil, message):
	global banbase,iq_request
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':affil})])])
	iq_request[iqid]=(time.time(),'','')
	sender(i)
	insl = GT('inlist_sleep_time')
	while not banbase.count(('TheEnd', 'None', iqid)): sleep(insl)
	iq_request.pop(iqid)
	bb,cc = [],[]
	for b in banbase: 
		if b[2] == iqid:
			if b[0] != 'TheEnd': bb.append(b)
		else: cc.append(b)
	banbase = cc
	msg = message % str(len(bb))
	if text != '':
		msg += ', '
		mmsg, cnt = '', 1
		for i in bb:
			if i[0].lower().count(text.lower()) or i[1].lower().count(text.lower()):
				mmsg += '\n%s. %s' % (cnt,i[0])
				if len(i[1]): mmsg += ' - %s' % i[1]
				cnt += 1
		if len(mmsg): msg += L('Found:') + mmsg
		else: msg += L('no matches!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(7, 'inban', inban, 2, L('Search in outcast list of conference.')),
	 (7, 'inmember', inmember, 2, L('Search in members list of conference.')),
	 (7, 'inadmin', inadmin, 2, L('Search in admins list of conference.')),
	 (7, 'inowner', inowner, 2, L('Search in owners list of conference.'))]
