#!/usr/bin/python
# -*- coding: utf -*-

def iq_vcard(type, jid, nick, text):
	global iq_answer
	if text.count('\n'):
		args = text.split('\n')[1]
		text = text.split('\n')[0]
	else: args = ''
	if text == '': who = getRoom(jid)+'/'+nick
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = getRoom(jid)+'/'+text
				break
	iqid = str(randint(1,100000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_VCARD},[])])
	sender(i)
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
	try: er_code = is_answ[1]
	except: er_code = None
	if to > 0:
		if is_answ[0] == None: msg = L('I can\'t do it')
		elif er_code == 'error': msg = is_answ[0]
		else:
			isa = is_answ[0]
			while isa.count('<BINVAL>') and isa.count('</BINVAL>'): isa=isa[:isa.find('<BINVAL>')]+isa[isa.find('</BINVAL>')+9:]
			if args.lower() == 'show':
				msg = L('vCard tags:') + ' '
				for i in range(0,len(isa)):
					if isa[i] == '<':
						tag = isa[i+1:isa.find('>',i)]
						if isa[i:].count('</'+tag+'>'): msg += tag+', '
				msg = msg[:-2]
			elif args != '':
				msg = L('vCard:') + ' '
				for tmp in args.split('|'):
					if tmp.count(':'): tname,ttag = tmp.split(':')[1],tmp.split(':')[0]
					else: tname,ttag = tmp,tmp
					tt = get_tag(isa,ttag.upper())
					if tt != '': msg += '\n'+tname+': '+rss_del_nn(rss_del_html(tt.replace('><','> <').replace('>\n<','> <')))
			else:
				msg = ''
				for tmp in [(L('Nick'),'NICKNAME'),(L('Name'),'FN'),(L('About'),'DESC'),(L('URL'),'URL')]:
					tt = get_tag(isa,tmp[1])
					if len(tt): msg += '\n'+tmp[0]+': '+tt
				if len(msg): msg = L('vCard:') + msg
				else: msg = L('Пусто!')
	else: msg = L('Timeout %s sec.') % str(timeout)
	send_msg(type, jid, nick, msg)

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
	sender(i)
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
	try: er_code = is_answ[1]
	except: er_code = None
	if er_code == 'error': msg = is_answ[0]
	elif to > 0:
		if iiqq == ['None']: msg = L('I can\'t do it')
		else:
			try: msg = L('Uptime: %s') % un_unix(int(iiqq[0].split('seconds="')[1].split('"')[0]))
			except: msg = L('I can\'t do it')
	else: msg = L('Timeout %s sec.') % str(timeout)
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
	sender(i)
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
	try: er_code = is_answ[1]
	except: er_code = None
	iiqq = []
	for iiq in is_answ:
		if iiq != None: iiqq.append(iiq)
		else: iiqq.append('None')
	if er_code == 'error': msg = is_answ[0]
	elif to > 0:
		if iiqq == ['None']: msg = L('I can\'t do it')
		else:
			tpi = ct-lt
			tpi = str(int(tpi))+'.'+str(int((tpi-int(tpi))*100))
			if sping: msg = L('Ping from you %s sec.') % tpi
			else: msg = L('Ping from %s %s sec.') % (text, tpi)
	else: msg = L('Timeout %s sec.') % str(timeout)
	send_msg(type, jid, nick, msg)

def iq_time(type, jid, nick, text):
	iq_time_get(type, jid, nick, text, None)

def iq_time_raw(type, jid, nick, text):
	iq_time_get(type, jid, nick, text, True)

def iq_time_get(type, jid, nick, text, mode):
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
	sender(i)
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
	try: er_code = is_answ[1]
	except: er_code = None
	if er_code == 'error': msg = is_answ[0]
	elif to > 0:
		if len(iiqq) == 3:
			msg = iiqq[0]
			if mode: msg += ', Raw time: '+iiqq[1]+', TimeZone: '+iiqq[2]
		else:
			msg = ''
			for iiq in iiqq: msg += iiq+' '
	else: msg = L('Timeout %s sec.') % str(timeout)
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
	sender(i)
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
	try: er_code = is_answ[1]
	except: er_code = None
	if er_code == 'error': msg = is_answ[0]
	elif to > 0:
		if len(iiqq) == 3: msg = iiqq[0]+' '+iiqq[1]+' // '+iiqq[2]
		else:
			msg = ''
			for iiq in iiqq: msg += iiq+' '
	else: msg = L('Timeout %s sec.') % str(timeout)
	send_msg(type, jid, nick, msg)

def iq_stats(type, jid, nick, text):
	global iq_answer
	if text == '':
			send_msg(type, jid, nick, u'Ась?')
			return
	iqid = str(randint(1,100000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':text}, payload = [Node('query', {'xmlns': NS_STATS},[Node('stat', {'name':'users/total'},[]),Node('stat', {'name':'users/online'},[])])])
	sender(i)
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
	try: er_code = is_answ[1]
	except: er_code = None
	if er_code == 'error': msg = is_answ[0]
	elif to > 0:
		if iiqq == 'None': ans = [0,0]
		else:
			try: ans = [get_subtag(iiqq.split('stat ')[1],'value'),get_subtag(iiqq.split('stat ')[2],'value')]
			except: ans = [0,0]
		msg = L('Server statistic: %s | Total: %s | Online: %s') % \
			(text, str(ans[1]), str(ans[0]))
	else: msg = L('Timeout %s sec.') % str(timeout)
	send_msg(type, jid, nick, msg)
	
global execute

execute = [(0, u'ver', iq_version, 2, L('Client version.')),
	 (0, u'ping', ping, 2, L('Ping - reply time. You can ping nick in room, jid, server or transport.')),
	 (0, u'time', iq_time, 2, L('Client side time.')),
	 (0, u'time_raw', iq_time_raw, 2, L('Client side time + raw time format.')),
	 (0, u'stats', iq_stats, 2, L('Users server statistic.')),
	 (0, u'vcard_raw', iq_vcard, 2, L('vCard query. Recomends make command base alias for query needs info.\nvcard_raw [nick] - query generic info\nvcard_raw nick\nshow - show available fields\nvcard_raw nick\n[field:name|field:name] - show requested fields from vcard.')),
	 (0, u'uptime', iq_uptime, 2, L('Server or jid uptime.'))]
