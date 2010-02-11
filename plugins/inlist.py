#!/usr/bin/python
# -*- coding: utf -*-

def inban(type, jid, nick, text):
	global banbase
	iqid = str(randint(1,1000000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'outcast'})])])
	cl.send(i)
	while not banbase.count((u'TheEnd', u'None', iqid)): sleep(0.1)
	bb = []
	for b in banbase:
		if b[2] == iqid and b[0] != u'TheEnd': bb.append(b)
	for b in banbase:
		if b[2] == iqid: banbase.remove(b)
	msg = L('Total banned: %s, ')+str(len(bb))
	if text != '':
		mmsg = L('found:\n')
		fnd = 1
		cnt = 1
		for i in bb:
			if i[0].lower().count(text.lower()) or i[1].lower().count(text.lower()):
				mmsg += str(cnt)+'. '+i[0]+' - '+i[1]+'\n'
				fnd = 0
				cnt += 1
		mmsg = mmsg[:-1]
		if fnd: mmsg = L('no matches!')
		msg += mmsg
	send_msg(type, jid, nick, msg)

def inowner(type, jid, nick, text):
	global banbase
	iqid = str(randint(1,1000000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'owner'})])])
	cl.send(i)
	while not banbase.count((u'TheEnd', u'None', iqid)): sleep(0.1)
	bb = []
	for b in banbase:
		if b[2] == iqid and b[0] != u'TheEnd': bb.append(b)
	for b in banbase:
		if b[2] == iqid: banbase.remove(b)
	msg = L('Total owners: %s, ') % str(len(bb))
	if text != '':
		mmsg = L('found:\n')
		fnd = 1
		cnt = 1
		for i in bb:
			if i[0].lower().count(text.lower()) or i[1].lower().count(text.lower()):
				mmsg += str(cnt)+'. '+i[0]+' - '+i[1]+'\n'
				fnd = 0
				cnt += 1
		mmsg = mmsg[:-1]
		if fnd: mmsg = L('no matches!')
		msg += mmsg
	send_msg(type, jid, nick, msg)

def inadmin(type, jid, nick, text):
	global banbase
	iqid = str(randint(1,1000000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'admin'})])])
	cl.send(i)
	while not banbase.count((u'TheEnd', u'None', iqid)): sleep(0.1)
	bb = []
	for b in banbase:
		if b[2] == iqid and b[0] != u'TheEnd': bb.append(b)
	for b in banbase:
		if b[2] == iqid: banbase.remove(b)
	msg = L('Total admins: %s, ') % str(len(bb))
	if text != '':
		mmsg = L('found:\n')
		fnd = 1
		cnt = 1
		for i in bb:
			if i[0].lower().count(text.lower()) or i[1].lower().count(text.lower()):
				mmsg += str(cnt)+'. '+i[0]+' - '+i[1]+'\n'
				fnd = 0
				cnt += 1
		mmsg = mmsg[:-1]
		if fnd: mmsg = L('no matches!')
		msg += mmsg
	send_msg(type, jid, nick, msg)

def inmember(type, jid, nick, text):
	global banbase
	iqid = str(randint(1,1000000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'member'})])])
	cl.send(i)
	while not banbase.count((u'TheEnd', u'None', iqid)): sleep(0.1)
	bb = []
	for b in banbase:
		if b[2] == iqid and b[0] != u'TheEnd': bb.append(b)
	for b in banbase:
		if b[2] == iqid: banbase.remove(b)

	msg = L('Total members: %s, ') % str(len(bb))
	if text != '':
		mmsg = L('found:\n')
		fnd = 1
		cnt = 1
		for i in bb:
			if i[0].lower().count(text.lower()) or i[1].lower().count(text.lower()):
				mmsg += str(cnt)+'. '+i[0]+' - '+i[1]+'\n'
				fnd = 0
				cnt += 1
		mmsg = mmsg[:-1]
		if fnd: mmsg = L('no matches!')
		msg += mmsg
	send_msg(type, jid, nick, msg)

global execute

execute = [(1, u'inban', inban, 2, L('Search in outcats list of conference.')),
	 (1, u'inmember', inmember, 2, L('Search in members list of conference.')),
	 (1, u'inadmin', inadmin, 2, L('Search in admins list of conference.')),
	 (1, u'inowner', inowner, 2, L('Search in owners list of conference.'))]
