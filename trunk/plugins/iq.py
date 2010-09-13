#!/usr/bin/python
# -*- coding: utf -*-

def iq_vcard(type, jid, nick, text):
	global iq_request
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
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_VCARD},[])])
	iq_request[iqid]=(time.time(),vcard_async,[type, jid, nick, text, args])
	sender(i)

def vcard_async(type, jid, nick, text, args, is_answ):
	isa = is_answ[1][0]
	while isa.count('<BINVAL>') and isa.count('</BINVAL>'): isa=isa[:isa.find('<BINVAL>')]+isa[isa.find('</BINVAL>')+9:]
	while isa.count('<PHOTO>') and isa.count('</PHOTO>'): isa=isa[:isa.find('<PHOTO>')]+isa[isa.find('</PHOTO>')+8:]
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
			if tt != '': msg += '\n'+tname+': '+rss_del_nn(remove_ltgt(tt.replace('><','> <').replace('>\n<','> <')))
	else:
		msg = ''
		for tmp in [(L('Nick'),'NICKNAME'),(L('Name'),'FN'),(L('About'),'DESC'),(L('URL'),'URL')]:
			tt = remove_ltgt(get_tag(isa,tmp[1]))
			if len(tt): msg += '\n'+tmp[0]+': '+tt
		if len(msg): msg = L('vCard:') + msg
		else: msg = L('Empty!')
	send_msg(type, jid, nick, msg)

def iq_uptime(type, jid, nick, text):
	global iq_request
	if text == '': who = getRoom(jid)+'/'+nick
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = getRoom(jid)+'/'+text
				break
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_LAST},[])])
	iq_request[iqid]=(time.time(),uptime_async,[type, jid, nick, text])
	sender(i)

def uptime_async(type, jid, nick, text, is_answ):
	isa = is_answ[1][0]
	try: msg = L('Uptime: %s') % un_unix(int(isa.split('seconds="')[1].split('"')[0]))
	except: msg = L('I can\'t do it')
	send_msg(type, jid, nick, msg)

def urn_ping(type, jid, nick, text):
	global iq_request
	if text == '': who = getRoom(jid)+'/'+nick
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = getRoom(jid)+'/'+text
				break
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('ping', {'xmlns': NS_URN_PING},[])])
	iq_request[iqid]=(time.time(),ping_async,[type, jid, nick, text])
	sender(i)

def ping(type, jid, nick, text):
	global iq_request
	if text == '': who = getRoom(jid)+'/'+nick
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = getRoom(jid)+'/'+text
				break
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_VERSION},[])])
	iq_request[iqid]=(time.time(),ping_async,[type, jid, nick, text])
	sender(i)
	
def ping_async(type, jid, nick, text, is_answ):
	tpi = float(is_answ[0])-time_nolimit
	tpi = str(int(tpi))+'.'+str(int((tpi-int(tpi))*10**GT('ping_digits')))
	if text == '': msg = L('Ping from you %s sec.') % tpi
	else: msg = L('Ping from %s %s sec.') % (text, tpi)
	send_msg(type, jid, nick, msg)
	
def iq_time(type, jid, nick, text):
	iq_time_get(type, jid, nick, text, None)

def iq_time_raw(type, jid, nick, text):
	iq_time_get(type, jid, nick, text, True)

def iq_time_get(type, jid, nick, text, mode):
	global iq_request
	if text == '': who = getRoom(jid)+'/'+nick
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = getRoom(jid)+'/'+text
				break
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_TIME},[])])
	iq_request[iqid]=(time.time(),time_async,[type, jid, nick, text, mode])
	sender(i)

def time_async(type, jid, nick, text, mode, is_answ):
	isa = is_answ[1]
	if len(isa) == 3:
		msg = isa[0]
		if mode: msg += ', Raw time: %s, TimeZone: %s' % (isa[1],isa[2])
	else: msg = ' '.join(isa)
	send_msg(type, jid, nick, msg)

def iq_utime(type, jid, nick, text):
	global iq_request
	if text == '': who = getRoom(jid)+'/'+nick
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = getRoom(jid)+'/'+text
				break
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('time', {'xmlns': NS_URN_TIME},[])])
	iq_request[iqid]=(time.time(),utime_async,[type, jid, nick, text])
	sender(i)

def utime_async(type, jid, nick, text, is_answ):
	isa = is_answ[1]
	ttup,tt = isa[0].replace('T','-').replace('Z','').replace(':','-').split('-')+['0','0',tuple(time.localtime())[8]],[]
	for tmp in ttup: tt.append(int(tmp))
	msg = nice_time(time.mktime(tuple(tt)) + (int(isa[1].split(':')[0])*60+int(isa[1].split(':')[1]))*60)[2]
	send_msg(type, jid, nick, msg)

def iq_version(type, jid, nick, text):
	global iq_request
	if text == '': who = getRoom(jid)+'/'+nick
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = getRoom(jid)+'/'+text
				break
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_VERSION},[])])
	iq_request[iqid]=(time.time(),version_async,[type, jid, nick, text])
	sender(i)

def version_async(type, jid, nick, text, is_answ):
	isa = is_answ[1]
	if len(isa) == 3: msg = '%s %s // %s' % isa
	else: msg = ' '.join(isa)
	send_msg(type, jid, nick, msg)

def iq_stats(type, jid, nick, text):
	global iq_request
	if text == '':
			send_msg(type, jid, nick, u'Ась?')
			return
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':text}, payload = [Node('query', {'xmlns': NS_STATS},[Node('stat', {'name':'users/total'},[]),Node('stat', {'name':'users/online'},[])])])
	iq_request[iqid]=(time.time(),stats_async,[type, jid, nick, text])
	sender(i)

def stats_async(type, jid, nick, text, is_answ):
	isa = unicode(is_answ[1])
	if isa == 'None': ans = [0,0]
	else:
		try: ans = [get_subtag(isa.split('stat ')[1],'value'),get_subtag(isa.split('stat ')[2],'value')]
		except: ans = [0,0]
	msg = L('Server statistic: %s | Total: %s | Online: %s') %  (text, str(ans[1]), str(ans[0]))
	send_msg(type, jid, nick, msg)
	
global execute

execute = [(3, u'ver', iq_version, 2, L('Client version.')),
	 (3, u'ping', ping, 2, L('Ping - reply time. You can ping nick in room, jid, server or transport.')),
	 (3, u'uping', urn_ping, 2, L('Ping - reply time. You can ping nick in room, jid, server or transport.')),
	 (3, u'time', iq_time, 2, L('Client side time.')),
	 (3, u'utime', iq_utime, 2, L('Client side time.')),
	 (3, u'time_raw', iq_time_raw, 2, L('Client side time + raw time format.')),
	 (3, u'stats', iq_stats, 2, L('Users server statistic.')),
	 (3, u'vcard_raw', iq_vcard, 2, L('vCard query. Recomends make command base alias for query needs info.\nvcard_raw [nick] - query generic info\nvcard_raw nick\nshow - show available fields\nvcard_raw nick\n[field:name|field:name] - show requested fields from vcard.')),
	 (3, u'uptime', iq_uptime, 2, L('Server or jid uptime.'))]
