#!/usr/bin/python
# -*- coding: utf-8 -*-

whereis_requests = []
whereis_answers	 = []
whereis_timeout  = 10
whereis_checks   = {}
whereis_lock	 = None

def disco(type, jid, nick, text):
	global iq_answer,iq_request
	text = reduce_spaces(text)
	if text == '':
		send_msg(type, jid, nick, L('What?'))
		return
	text = text.lower().split(' ')
	where = text[0]
	try: what = text[1]
	except: what = ''
	try: hm = int(text[2])
	except: hm = 10
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':where}, payload = [Node('query', {'xmlns': NS_DISCO_ITEMS},[])])
	iq_request[iqid]=(time.time(),disco_async,[type, jid, nick, what, where, hm])
	sender(i)

def disco_async(type, jid, nick, what, where, hm, is_answ):
	isan = unicode(is_answ[1][0])
	if isan != 'None':
		if (where.count('chat') or where.count('conference')) and not where.count('@'):
			tmp = sqlite3.connect(':memory:')
			cu = tmp.cursor()
			cu.execute('''create table tempo (nick text, room text, size text)''')
			isa = isan.split('<item ')
			for ii in isa[1:]:
				dname = get_subtag(ii,'name')
				djid = get_subtag(ii,'jid')
				dpos = 1
				for tmp2 in range(0,dname.count('(')): dpos = dname.find('(',dpos+1)
				dsize = dname[dpos+1:dname.find(')',dpos+1)]
				dname = dname[:-(len(dsize)+3)]
				cu.execute('insert into tempo values (?,?,?)', (dname, djid, dsize))
			if len(what): cm = cu.execute('select * from tempo where (nick like ? or room like ?) order by -size',('%'+what+'%','%'+what+'%')).fetchmany(hm)
			else: cm = cu.execute('select * from tempo order by -size').fetchmany(hm)
			if len(cm):
				cnt = 1
				msg = L('Total: %s') % len(cm)
				for i in cm:
					msg += u'\n%s. %s [%s] . %s' % (cnt,i[0],i[1],i[2])
					cnt += 1
			elif len(what): msg = L('\"%s\" not found') % what
			else: msg = L('Not found.')
			tmp.close()
		elif where.count('@conference') or where.count('@chat'):
			tmp = sqlite3.connect(':memory:')
			cu = tmp.cursor()
			cu.execute('''create table tempo (nick text)''')
			isa = isan.split('<item ')
			for ii in isa[1:]:
				dname = get_subtag(ii,'name')
				cu.execute('insert into tempo values (?)', (dname,))
			if len(what): cm = cu.execute('select * from tempo where (nick like ?) order by nick',('%'+what+'%',)).fetchall()
			else: cm = cu.execute('select * from tempo order by nick').fetchall()
			if len(cm):
				msg = L('Total: %s%s') % (str(len(cm)), ' - ')
				for i in cm: msg += i[0]+', '
				msg = msg[:-2]
			elif len(what): msg = L('\"%s\" not found') % what
			else: msg = L('Not found.')
			tmp.close()
		else:
			tmp = sqlite3.connect(':memory:')
			cu = tmp.cursor()
			cu.execute('''create table tempo (jid text)''')
			isa = isan.split('<item ')
			for ii in isa[1:]:
				djid = get_subtag(ii,'jid')
				cu.execute('insert into tempo values (?)', (djid,))
			cm = cu.execute('select * from tempo order by jid').fetchall()
			if len(cm):
				cnt = 1
				msg = L('Total: %s') % str(len(cm))
				for i in cm:
					msg += '\n%s. %s' % (cnt,i[0])
					cnt += 1
			else: msg = L('Not found.')
			tmp.close()
	else: msg = L('I can\'t do it')
	msg = rss_replace(msg)
	send_msg(type, jid, nick, msg)

def whereis(type, jid, nick, text):
	global iq_request,whereis_lock
	if whereis_lock:
		send_msg(type, jid, nick, L('This command in use somewhere else. Please try later.'))
	else:
		whereis_lock = True
		if len(text):
			text = text.split(' ')
			who = text[0]
		else: who = nick
		if len(text)<2: where = getServer(jid)
		else:
			if text[1].count('conference'): where = text[1]
			else: where = 'conference.'+text[1]
		iqid = get_id()
		i = Node('iq', {'id': iqid, 'type': 'get', 'to':where}, payload = [Node('query', {'xmlns': NS_DISCO_ITEMS},[])])	
		iq_request[iqid]=(time.time(),whereis_async,[type, jid, nick, who, where])
		sender(i)

def whereis_async(type, jid, nick, who, where, is_answ):
	global whereis_requests, whereis_checks, iq_request, whereis_answers, whereis_lock
	isan = unicode(is_answ[1][0])
	isa = isan.split('<item ')
	djids = []
	for ii in isa[1:]:
		dname = get_subtag(ii,'name').split('(')[-1]
		if dname != 'n/a)' and dname != '0)': djids.append(get_subtag(ii,'jid'))
	send_msg(type, jid, nick, L('Please wait. Result you will be receive in private message approximately %s %s') % (str(int(len(djids)/1.1)), L('sec.')))
	curr_id = 'whereis_%s' % get_id()
	whereis_checks[curr_id] = len(djids)
	for ii in djids:
		iqid, tt = get_id(), time.time()
		i = Node('iq', {'id': iqid, 'type': 'get', 'to':ii}, payload = [Node('query', {'xmlns': NS_DISCO_ITEMS},[])])
		iq_request[iqid]=(tt,whereis_collect_async,[who,tt, iqid, curr_id])
		whereis_requests.append((curr_id,iqid,tt))
		sender(i)
		# --- Контроль отправки ---
		cnt = whereis_timeout
		while cnt > 0:
			if (curr_id,iqid,tt) in whereis_requests:
				sleep(0.1)
				cnt -= 0.1
			else: break
		if not cnt:
			whereis_requests.remove((curr_id,iqid,tt))
			whereis_checks[curr_id] -= 1
			iq_request.pop(iqid)
		# -------------------------
	while whereis_checks[curr_id]:
		for tmp in whereis_requests:
			if tmp[0] == curr_id and time.time() > tmp[2] + whereis_timeout:
				whereis_requests.remove(tmp)
				whereis_checks[curr_id] -= 1
			break
	cm = []
	whereis_checks.pop(curr_id)
	for tmp in whereis_answers:
		if tmp[0] == curr_id:
			whereis_answers.remove(tmp)
			cm.append(tmp[1:])
	cm.sort()
	if len(cm):
		msgg = L('matches with nick \"%s\": %s') % (who, str(len(cm)))
		for i in cm: msgg += '\n'+i[0]+'\t'+i[1]
	else: msgg = L('nick \"%s\" not found.') % who
	msg = L('Total conferences: %s, available: %s') % (str(len(isa)-1), str(len(djids))+', '+msgg)
	send_msg('chat', jid, nick, msg)
	whereis_lock = None

def whereis_collect_async(who,tt,iqid,curr_id,is_answ):
		global whereis_requests,whereis_checks,whereis_answers
		whereis_requests.remove((curr_id,iqid,tt))
		whereis_checks[curr_id] -= 1
		isan = unicode(is_answ[1][0])
		isd = isan.split('<item ')
		for iii in isd[1:]:
			dname = get_subtag(iii,'name')
			if dname.lower().count(who.lower()): whereis_answers.append((curr_id, dname, getRoom(get_subtag(iii,'jid'))))

global execute

execute = [(0, 'disco', disco, 2, L('Service discovery.\ndisco server.tld - request information about server\ndisco conference.server.tld [body [size]] - find body string in conference list and show size results\ndisco room@conference.server.tld [body [size]] - find body string in disco room conference and show size results.')),
	 (1, 'whereis', whereis, 2, L('Find nick on conference server\nwhereis - find your nick on current conference server\nwhereis nick - find nick on current conference server\nwhereis nick [conference.]server.tld - find nick on server server.tld'))]
