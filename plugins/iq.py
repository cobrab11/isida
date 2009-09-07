#!/usr/bin/python
# -*- coding: utf -*-

def iq_uptime(type, jid, nick, text):
	global iq_answer
	if text == '': who = getRoom(jid)+'/'+nick
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = getRoom(jid)+'/'+text
				break
	iqid = str(randint(1,100000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_LAST},[])])
	cl.send(i)
	to = timeout
	no_answ = 1
	is_answ = [None]
	while to >= 0 and no_answ:
		for aa in iq_answer:
			if aa[0]==iqid:
				is_answ = aa[1:]
				iq_answer.remove(aa)
				no_answ = 0
				break
		sleep(0.05)
		to -= 0.05
	iiqq = []
	for iiq in is_answ: iiqq.append(unicode(iiq))
	if to > 0:
		if iiqq == ['None']: msg = u'Что-то не получается...'
		else:
			try: msg = u'Аптайм: '+un_unix(int(iiqq[0].split('seconds="')[1].split('"')[0]))
			except: msg = u'Что-то не получается...'

	else: msg = u'Истекло время ожидания ('+str(timeout)+u'сек).'
	send_msg(type, jid, nick, msg)

def ping(type, jid, nick, text):
	global iq_answer
	if text == '':
		sping = 1
		who = getRoom(jid)+'/'+nick
	else:
		sping = 0
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = getRoom(jid)+'/'+text
				break
	iqid = str(randint(1,100000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_VERSION},[])])
	cl.send(i)
	to = timeout
	lt = time.time()
	no_answ = 1
	is_answ = [None]
	while to >= 0 and no_answ:
		for aa in iq_answer:
			if aa[0]==iqid:
				is_answ = aa[1:]
				iq_answer.remove(aa)
				no_answ = 0
				break
		sleep(0.001)
		to -= 0.001
	ct = time.time()
	iiqq = []
	for iiq in is_answ:
		if iiq != None: iiqq.append(iiq)
		else: iiqq.append('None')
	if to > 0:
		if iiqq == ['None']: msg = u'Что-то не получается...'
		else:
			tpi = ct-lt
			tpi = str(int(tpi))+'.'+str(int((tpi-int(tpi))*10000))
			if sping: msg = u'Пинг от тебя '+tpi+u' сек.'
			else: msg = u'Пинг от '+text+' '+tpi+u' сек.'
	else: msg = u'Истекло время ожидания ('+str(timeout)+u'сек).'
	send_msg(type, jid, nick, msg)

def iq_time(type, jid, nick, text):
	global iq_answer
	if text == '': who = getRoom(jid)+'/'+nick
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = getRoom(jid)+'/'+text
				break
	iqid = str(randint(1,100000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_TIME},[])])
	cl.send(i)
	to = timeout
	no_answ = 1
	is_answ = [None]
	while to >= 0 and no_answ:
		for aa in iq_answer:
			if aa[0]==iqid:
				is_answ = aa[1:]
				iq_answer.remove(aa)
				no_answ = 0
				break
		sleep(0.5)
		to -= 0.5
	iiqq = []
	for iiq in is_answ: iiqq.append(unicode(iiq))
	if to > 0:
		if len(iiqq) == 3: msg = iiqq[0]+' (Raw time: '+iiqq[1]+' | TimeZone: '+iiqq[2]+')'
		else:
			msg = ''
			for iiq in iiqq: msg += iiq+' '
	else: msg = u'Истекло время ожидания ('+str(timeout)+u'сек).'
	send_msg(type, jid, nick, msg)

def iq_version(type, jid, nick, text):
	global iq_answer
	if text == '': who = getRoom(jid)+'/'+nick
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = getRoom(jid)+'/'+text
				break
	iqid = str(randint(1,100000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_VERSION},[])])
	cl.send(i)
	to = timeout
	no_answ = 1
	is_answ = [None]
	while to >= 0 and no_answ:
		for aa in iq_answer:
			if aa[0]==iqid:
				is_answ = aa[1:]
				iq_answer.remove(aa)
				no_answ = 0
				break
		sleep(0.5)
		to -= 0.5
	iiqq = []
	for iiq in is_answ: iiqq.append(unicode(iiq))
	if to > 0:
		if len(iiqq) == 3: msg = iiqq[0]+' '+iiqq[1]+' // '+iiqq[2]
		else:
			msg = ''
			for iiq in iiqq: msg += iiq+' '
	else: msg = u'Истекло время ожидания ('+str(timeout)+u'сек).'
	send_msg(type, jid, nick, msg)

def iq_stats(type, jid, nick, text):
	global iq_answer
	if text == '':
			send_msg(type, jid, nick, u'Ась?')
			return
	iqid = str(randint(1,100000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':text}, payload = [Node('query', {'xmlns': NS_STATS},[Node('stat', {'name':'users/total'},[]),Node('stat', {'name':'users/online'},[])])])
	cl.send(i)
	to = timeout
	no_answ = 1
	is_answ = [None]
	while to >= 0 and no_answ:
		for aa in iq_answer:
			if aa[0]==iqid:
				is_answ = aa[1:]
				iq_answer.remove(aa)
				no_answ = 0
				break
		sleep(0.25)
		to -= 0.25
	iiqq = unicode(is_answ)
	if to > 0: 
		if iiqq == 'None': ans = [0,0]
		else:
			try: ans = [get_subtag(iiqq.split('stat ')[1],'value'),get_subtag(iiqq.split('stat ')[2],'value')]
			except: ans = [0,0]
		msg = u'Статистика сервера: '+text+u' | Всего: '+str(ans[1])+u' | Онлайн: '+str(ans[0])
	else: msg = u'Истекло время ожидания ('+str(timeout)+u'сек).'
	send_msg(type, jid, nick, msg)
	
global execute

execute = [(0, u'ver', iq_version, 2, u'Версия клиента'),
	 (0, u'ping', ping, 2, u'Пинг - время отклика. Можно пинговать ник в конференции, jid, сервер, транспорт.'),
	 (0, u'time', iq_time, 2, u'Локальное время клиента'),
	 (0, u'stats', iq_stats, 2, u'Статистика пользователей сервера'),
	 (0, u'uptime', iq_uptime, 2, u'Аптайм jabber сервера или jid\'а')]
