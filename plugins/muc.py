#!/usr/bin/python
# -*- coding: utf -*-

# -------------- affiliation -----------------

def global_ban(type, jid, nick, text):
	text = text.lower()
	hroom = getRoom(jid)
	hr = getFile(ignoreban,[])
	al = get_level(jid,nick)[0]
	if al == 9: af = 'owner'
	else: af = get_affiliation(jid,nick)
	if af != 'owner': msg = L('This command available only for conference owner!')
	elif text == 'show' and al == 9:
		if len(hr):
			msg = L('Global ban is off in:')
			for tmp in hr: msg += '\n'+tmp
		else: msg = L('Global ban enable without limits!')
	elif text == 'del' and af == 'owner':
		if hr.count(hroom): msg = L('Conference %s already deleted from global ban list!') % hroom
		else:
			hr.append(hroom)
			msg = L('Conference %s has been deleted from global ban list!') % hroom
			writefile(ignoreban,str(hr))
	elif text == 'add' and af == 'owner':
		if hr.count(hroom):
			hr.remove(hroom)
			msg = L('Conference %s has been added from global ban list!') % hroom
			writefile(ignoreban,str(hr))
		else: msg = L('Conference %s already exist in global ban list!') % hroom
	else:
		if al == 9:
			if hroom in hr: msg = L('Your conference will be ignored for global ban!')
			elif not text.count('@') or not text.count('.'): msg = L('I need jid!')
			else:
				reason = L('banned global by %s from %s') % (nick, jid)
				for tmp in confbase:
					if not (getRoom(tmp) in hr):
						i = Node('iq', {'id': get_id(), 'type': 'set', 'to':getRoom(tmp)}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'outcast', 'jid':unicode(text)},[Node('reason',{},reason)])])])
						sender(i)
						sleep(0.1)
				msg = L('jid %s has been banned in %s conferences.') % (text, str(len(confbase)-len(hr)))
		else: msg = L('Command temporary blocked!')
	send_msg(type, jid, nick, msg)

def muc_tempo_ban(type, jid, nick,text):
	if text[:4].lower() == 'show' and not text.count('\n'):
		text = text[5:]
		if not len(text): text = '.'
		ubl = getFile(tban,[])
		msg = ''
		for ub in ubl:
			if ub[0] == jid and ub[1].count(text.lower()): msg += '\n'+ub[1]+'\t'+un_unix(ub[2]-int(time.time()))
		if len(msg): msg = L('Found: %s') % msg
		else: msg = L('Not found.')
		send_msg(type, jid, nick, msg)

	elif text[:3].lower() == 'del' and not text.count('\n'):
		text = text[4:]
		if not len(text): text = '@@'
		ubl = getFile(tban,[])
		msg = ''
		for ub in ubl:
			if ub[0] == jid and ub[1] == text.lower():
				msg += ub[1]+'\t'+un_unix(ub[2]-int(time.time()))
				i = Node('iq', {'id': get_id(), 'type': 'set', 'to':ub[0]}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'none', 'jid':getRoom(unicode(ub[1]))},[])])])
				sender(i)
				ubl.remove(ub)
		if len(msg):
			msg = L('Removed: %s') % msg
			writefile(tban,str(ubl))
		else: msg = L('Not found.')
		send_msg(type, jid, nick, msg)
	else: muc_tempo_ban2(type, jid, nick,text)

def muc_tempo_ban2(type, jid, nick,text):
	skip = None
	if len(text):
		who = text.split('\n',2)[0]
		try:
			ttime = text.split('\n',2)[1]
			tttime = int(ttime[:-1])
			tmode = ttime[-1:].lower()
			tkpd = {'s':1, 'm':60, 'h':3600, 'd':86400}
			tttime = tttime*tkpd[tmode]
		except: tttime = 0
		if tttime:
			try: reason = text.split('\n',2)[2]
			except: reason = L('No reason!')
			reason = L('ban on %s since %s because %s') % \
				(un_unix(tttime), timeadd(tuple(localtime())), reason)
			mdb = sqlite3.connect(agestatbase)
			cu = mdb.cursor()
			fnd = cu.execute('select jid from age where room=? and (nick=? or jid=?) group by jid',(jid,who,who)).fetchall()
			if len(fnd) == 1: msg, whojid = L('done'), getRoom(unicode(fnd[0][0]))
			elif len(fnd) > 1:
				whojid = getRoom(get_level(jid,who)[1])
				if whojid != 'None': msg = L('done')
				else: msg, skip = L('I seen some peoples with this nick. Get more info!'), True
			else:
				if who.count('.'):
					msg = L('I don\'n know %s, and use as is!') % who
					whojid = who
				else: msg, skip = L('I don\'t know %s') % who , True
		else: msg, skip = L('Time format error!'), True
	else: msg, skip = L('What?'), True

	if skip: send_msg(type, jid, nick, msg)
	else:
		i = Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'outcast', 'jid':unicode(whojid)},[Node('reason',{},reason)])])])
		sender(i)

		ubl = getFile(tban,[])
		for ub in ubl:
			if ub[0] == jid and ub[1] == whojid: ubl.remove(ub)
		ubl.append((jid,whojid,tttime+int(time.time())))
		writefile(tban,str(ubl))
		send_msg(type, jid, nick, msg)

def muc_ban(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'outcast')
def muc_none(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'none')
def muc_member(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'member')

def muc_affiliation(type, jid, nick, text, aff):
	tmppos = arr_semi_find(confbase, jid)
	if tmppos == -1: nowname = nickname
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '': nowname = nickname
	xtype = ''
	for base in megabase:
		if base[0].lower() == jid and base[1] == nowname:
			xtype = base[3]
			break
	if xtype == 'owner':
		send_msg(type, jid, nick, L('Command is locked!'))
	elif len(text):
		skip = None
		if text.count('\n'): who, reason = text.split('\n',1)[0], text.split('\n',1)[1]
		else: who, reason = text, L('by Isida!')
		whojid = unicode(get_level(jid,who)[1])
		if whojid != 'None': sender(Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':aff, 'jid':whojid},[Node('reason',{},reason)])])]))
		else: send_msg(type, jid, nick, L('I don\'t know %s') % who)
	else: send_msg(type, jid, nick, L('What?'))

def muc_ban_past(type, jid, nick,text): muc_affiliation_past(type, jid, nick, text, 'outcast')
def muc_none_past(type, jid, nick,text): muc_affiliation_past(type, jid, nick, text, 'none')
def muc_member_past(type, jid, nick,text): muc_affiliation_past(type, jid, nick, text, 'member')

def muc_affiliation_past(type, jid, nick, text, aff):
	tmppos = arr_semi_find(confbase, jid)
	if tmppos == -1: nowname = nickname
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '': nowname = nickname
	xtype = ''
	for base in megabase:
		if base[0].lower() == jid and base[1] == nowname:
			xtype = base[3]
			break
	if xtype == 'owner': msg, text = L('Command is locked!'), ''
	else: msg = L('What?')
	if len(text):
		skip = None
		if text.count('\n'): who, reason = text.split('\n',1)[0], text.split('\n',1)[1]
		else: who, reason = text, L('by Isida!')
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		fnd = cu.execute('select jid from age where room=? and (nick=? or jid=?) group by jid',(jid,who,who)).fetchall()
		if len(fnd) == 1: msg, whojid = L('done'), getRoom(unicode(fnd[0][0]))
		elif len(fnd) > 1:
			whojid = getRoom(get_level(jid,who)[1])
			if whojid != 'None': msg = L('done')
			else: msg, skip = L('I seen some peoples with this nick. Get more info!'), True
		else:
			msg = L('I don\'n know %s, and use as is!') % who
			whojid = who
	else: skip = True
	if skip: send_msg(type, jid, nick, msg)
	else:
		i = Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':aff, 'jid':unicode(whojid)},[Node('reason',{},reason)])])])
		sender(i)
		send_msg(type, jid, nick, msg)

def muc_kick(type, jid, nick, text): muc_role(type, jid, nick, text, 'none')
def muc_participant(type, jid, nick, text): muc_role(type, jid, nick, text, 'participant')
def muc_visitor(type, jid, nick, text): muc_role(type, jid, nick, text, 'visitor')
def muc_moderator(type, jid, nick, text): muc_role(type, jid, nick, text, 'moderator')

def muc_role(type, jid, nick, text, role):
	tmppos = arr_semi_find(confbase, jid)
	if tmppos == -1: nowname = nickname
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '': nowname = nickname
	xtype = ''
	for base in megabase:
		if base[0].lower() == jid and base[1] == nowname:
			xtype = base[3]
			break
	if xtype == 'owner':
		send_msg(type, jid, nick, L('Command is locked!'))
	elif len(text):
		skip = None
		if text.count('\n'): who, reason = text.split('\n',1)[0], text.split('\n',1)[1]
		else: who, reason = text, L('by Isida!')
		whojid = unicode(get_level(jid,who)[1])
		if whojid != 'None': sender(Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':role, 'jid':whojid},[Node('reason',{},reason)])])]))
		else: send_msg(type, jid, nick, L('I don\'t know %s') % who)
	else: send_msg(type, jid, nick, L('What?'))

def check_unban():
	unban_log = getFile(tban,[])
	if unban_log != '[]':
		ubl = []
		for ub in unban_log:
			if ub[2] > int(time.time()): ubl.append(ub)
			else:
				i = Node('iq', {'id': get_id(), 'type': 'set', 'to':ub[0]}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'none', 'jid':getRoom(unicode(ub[1]))},[])])])
				sender(i)
		if unban_log != ubl: writefile(tban,str(ubl))

global execute, timer

timer = [check_unban]

execute = [(7, 'ban_past', muc_ban_past, 2, L('Ban user.')),
	   (7, 'ban', muc_ban, 2, L('Ban user.')),
	   (7, 'tban', muc_tempo_ban, 2, L('Temporary ban.\ntban show|del [jid] - show/del temporary bans\ntban nick\ntimeD|H|M|S\nreason - ban nick for time because reason.')),
	   (7, 'none_past', muc_none_past, 2, L('Delete user affiliation.')),
	   (7, 'member_past', muc_member_past, 2, L('Get member affiliation.')),
	   (7, 'none', muc_none, 2, L('Delete user affiliation.')),
	   (7, 'member', muc_member, 2, L('Get member affiliation.')),
	   (7, 'kick', muc_kick, 2, L('Kick user.')),
	   (7, 'participant', muc_participant, 2, L('Give participant.')),
	   (7, 'visitor', muc_visitor, 2, L('Give visitor.')),
	   (7, 'moderator', muc_moderator, 2, L('Give role moderator.')),
	   (8, 'global_ban', global_ban, 2, L('Global ban. Available only for confernce owner.\nglobal_ban del - remove conference from banlist,\nglobal_ban add - add conference into banlist,\nglobal_ban <jid> - ban jid in all rooms, where bot is admin.'))]
