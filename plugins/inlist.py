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
	msg = u'Всего в бане: '+str(len(bb))
	if text != '':
		mmsg = u', найдено:\n'
		fnd = 1
		cnt = 1
		for i in bb:
			if i[0].lower().count(text.lower()) or i[1].lower().count(text.lower()):
				mmsg += str(cnt)+'. '+i[0]+' - '+i[1]+'\n'
				fnd = 0
				cnt += 1
		mmsg = mmsg[:-1]
		if fnd: mmsg = u', совпадений нет!'
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
	msg = u'Всего владельцев: '+str(len(bb))
	if text != '':
		mmsg = u', найдено:\n'
		fnd = 1
		cnt = 1
		for i in bb:
			if i[0].lower().count(text.lower()) or i[1].lower().count(text.lower()):
				mmsg += str(cnt)+'. '+i[0]+' - '+i[1]+'\n'
				fnd = 0
				cnt += 1
		mmsg = mmsg[:-1]
		if fnd: mmsg = u', совпадений нет!'
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
	msg = u'Всего администраторов: '+str(len(bb))
	if text != '':
		mmsg = u', найдено:\n'
		fnd = 1
		cnt = 1
		for i in bb:
			if i[0].lower().count(text.lower()) or i[1].lower().count(text.lower()):
				mmsg += str(cnt)+'. '+i[0]+' - '+i[1]+'\n'
				fnd = 0
				cnt += 1
		mmsg = mmsg[:-1]
		if fnd: mmsg = u', совпадений нет!'
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

	msg = u'Всего постоянных участников: '+str(len(bb))
	if text != '':
		mmsg = u', найдено:\n'
		fnd = 1
		cnt = 1
		for i in bb:
			if i[0].lower().count(text.lower()) or i[1].lower().count(text.lower()):
				mmsg += str(cnt)+'. '+i[0]+' - '+i[1]+'\n'
				fnd = 0
				cnt += 1
		mmsg = mmsg[:-1]
		if fnd: mmsg = u', совпадений нет!'
		msg += mmsg
	send_msg(type, jid, nick, msg)

global execute

execute = [(1, u'inban', inban, 2, u'Поиск по outcast списку конференции.'),
	 (1, u'inmember', inmember, 2, u'Поиск по member списку конференции.'),
	 (1, u'inadmin', inadmin, 2, u'Поиск по admin списку конференции.'),
	 (1, u'inowner', inowner, 2, u'Поиск по owner списку конференции.')]
