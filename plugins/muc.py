#!/usr/bin/python
# -*- coding: utf -*-

tban = set_folder+'temporary.ban'		# лог временного бана
af_alist = set_folder+'alist.aff'		# alist аффиляций
ro_alist = set_folder+'alist.rol'		# alist ролей
ignoreban = set_folder+'ignoreban.db'	# список игнора при глобальном бане

# -------------- affiliation -----------------

def global_ban(type, jid, nick, text):
	text = text.lower()
	hroom = getRoom(jid)
	hr = getFile(ignoreban,[])
	al = get_access(jid,nick)[0]
	if al == 2: af = 'owner'
	else: af = get_affiliation(jid,nick)
	if af != 'owner': msg = L('This command available only for conference owner!')
	elif text == 'show' and al == 2:
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
				whojid = getRoom(get_access(jid,who)[1])
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
def muc_admin(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'admin')
def muc_owner(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'owner')

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
			whojid = getRoom(get_access(jid,who)[1])
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

# -------------- role -----------------

def muc_kick(type, jid, nick,text): muc_role(type, jid, nick, text, 'none')
def muc_participant(type, jid, nick,text): muc_role(type, jid, nick, text, 'participant')
def muc_visitor(type, jid, nick,text): muc_role(type, jid, nick, text, 'visitor')
def muc_moderator(type, jid, nick,text): muc_role(type, jid, nick, text, 'moderator')

def muc_role(type, jid, nick, text, role):
	skip = None
	if len(text):
		if text.count('\n'): who, reason = text.split('\n',1)[0], text.split('\n',1)[1]
		else: who, reason = text, L('by Isida!')
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		fnd = cu.execute('select nick from age where room=? and (nick=? or jid=?) group by jid',(jid,who,who)).fetchall()
		if len(fnd) == 1: whonick, msg = unicode(fnd[0][0]), L('done')
		elif len(fnd) > 1:
			wj = getRoom(get_access(jid,who)[1])
			if wj != 'None': whonick, msg = who, L('done')
			else: msg, skip = L('I seen some peoples with this nick. Get more info!'), True
		else: 
			msg = L('I don\'n know %s, and use as is!') % who
			whonick = who
	else: msg, skip = L('What?'), True
	if skip: send_msg(type, jid, nick, msg)
	else:
		i = Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':role, 'nick':unicode(whonick)},[Node('reason',{},reason)])])])
		sender(i)
		send_msg(type, jid, nick, msg)

# ----------------------------------------------
# role nick
# time
# reason

def muc_akick(type, jid, nick,text): muc_arole(type, jid, nick, text, 'none')
def muc_aparticipant(type, jid, nick,text): muc_arole(type, jid, nick, text, 'participant')
def muc_avisitor(type, jid, nick,text): muc_arole(type, jid, nick, text, 'visitor')
def muc_amoderator(type, jid, nick,text): muc_arole(type, jid, nick, text, 'moderator')

def muc_arole(type, jid, nick, text, role):
	skip = True
	if len(text):
		if text[:4].lower() == 'show' and not text.count('\n'):
			text = text[5:]
			if not len(text): text = '.'
			alist_role = getFile(ro_alist,[])
			msg = ''
			if alist_role != '[]':
				for tmp in alist_role:
					if tmp[0] == jid and tmp[3] == role and tmp[2].count(text.lower()):
						msg += '\n'+tmp[2]+'\t'+tmp[4]+' (by '+tmp[1]+')'
						if tmp[5]: msg += '\t'+un_unix(tmp[5]-int(time.time()))
			if not len(msg):
				if text == '.': msg = L('List is empty')
				else: msg = L('Not found.')
		elif text[:4].lower() == 'del ' and not text.count('\n'):
			text = text[4:]
			if not len(text): msg = L('Who delete?')
			else:
				msg = L('Not found.')
				alist_role = getFile(ro_alist,[])
				for tmp in alist_role:
					if tmp[0] == jid and (tmp[2] == role or tmp[2] == text):
						alist_role.remove(tmp)
						writefile(ro_alist,str(alist_role))
						msg = L('Removed: %s') % tmp[2]
						break
		elif text.lower() == 'clear':
			alist_role = getFile(ro_alist,[])
			tmp_role = []
			for tmp in alist_role:
				if tmp[0] != jid: tmp_role.append(tmp)
			writefile(ro_alist,str(tmp_role))
			msg = L('Cleared for %s') % str(jid)
		else:
			who = text.split('\n',2)[0]
			try:
				ttime = text.split('\n',2)[1]
				tttime = int(ttime[:-1])
				tmode = ttime[-1:].lower()
				tkpd = {'s':1, 'm':60, 'h':3600, 'd':86400}
				tttime = tttime*tkpd[tmode]
			except:
				tttime = 0
				try: reason = text.split('\n',2)[1]
				except: reason = L('No reason!')
			if tttime:
				try: reason = text.split('\n',2)[2]
				except: reason = L('No reason!')
			mdb = sqlite3.connect(agestatbase)
			cu = mdb.cursor()
			fnd = cu.execute('select nick,jid from age where room=? and (nick=? or jid=?) group by jid',(jid,who,who)).fetchall()
			if len(fnd) == 1: whonick, whojid, skip, msg = unicode(fnd[0][0]), unicode(fnd[0][1]), None, L('done')
			elif len(fnd) > 1:
				whojid = getRoom(get_access(jid,who)[1])
				if whojid != 'None': whonick, msg, skip = who, L('done'), None
				else: msg = L('I seen some peoples with this nick. Get more info!')
			else: msg = L('I don\'t know %s') % who
	else: msg = L('What?')
	
	if skip: send_msg(type, jid, nick, msg)
	else:
		alist_role = getFile(ro_alist,[])
		for tmp in alist_role:
			if tmp[0] == jid and tmp[2] == whojid: alist_role.remove(tmp)
		if tttime: alist_role.append((jid,nick,whojid,role,reason,tttime+int(time.time())))
		else: alist_role.append((jid,nick,whojid,role,reason,0))
		i = Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':role, 'nick':unicode(whonick)},[Node('reason',{},reason)])])])
		sender(i)
		writefile(ro_alist,str(alist_role))
		send_msg(type, jid, nick, L('done'))
# ----------------------------------------------

# room, jid, time

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

def decrease_alist_role():
	alist_role = getFile(ro_alist,[])
	if alist_role != []:
		tmp_role = []
		for tmp in alist_role:
			if tmp[5] == 0 or tmp[5] > int(time.time()): tmp_role.append(tmp)
		if alist_role != tmp_role: writefile(ro_alist,str(tmp_role))

# ----------------------------------------------
def muc_afind(type, jid, nick, text):
	skip = None
	if len(text):
		who = text
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		fnd = cu.execute('select nick,jid from age where room=? and (nick=? or jid=?) group by jid',(jid,who,who)).fetchall()
		if len(fnd) == 1: whonick, whojid, skip = unicode(fnd[0][0]), unicode(fnd[0][1]), True
		elif len(fnd) > 1:
			whojid = getRoom(get_access(jid,who)[1])
			if whojid != 'None': whonick, msg, skip = who, L('done'), True
			else: msg = L('I seen some peoples with this nick. Get more info!')
		else: msg = L('I don\'t know %s') % who
	else: msg = L('What?')
	if skip:
		alist_role = getFile(ro_alist,[])
		not_found = 1
		for tmp in alist_role:
			if tmp[0] == jid and tmp[2] == whojid:
				msg = L('Found in list: %s %s, reason: %s by %s') % (tmp[3], '('+tmp[2]+')', tmp[4], '('+tmp[1]+')')
				if tmp[5]: msg += ' '+un_unix(tmp[5]-int(time.time()))
				not_found = 0
				break
		if not_found: msg = L('No matches for %s in alist.') % text
	send_msg(type, jid, nick, msg)

# ----------------------------------------------
#room,jid,nick,type,text

def alist_role_presence(room,jid,nick,type,text):
#	print 'presence:',room,jid,nick,type,text
	alist_role = getFile(ro_alist,[])
	jid = getRoom(jid)
	if alist_role != []:
		for tmp in alist_role:
			if tmp[0] == room and tmp[2] == jid:
				i = Node('iq', {'id': get_id(), 'type': 'set', 'to':tmp[0]}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':tmp[3], 'nick':unicode(nick)},[Node('reason',{},tmp[4])])])])
				sender(i)
				break

#def alist_message(room,jid,nick,type,text):
#	print 'message:',room,jid,nick,type,text

# ----------------------------------------------

global execute, timer, presence_control#, message_control

timer = [check_unban,decrease_alist_role]
presence_control = [alist_role_presence]
#message_control = [alist_message]

execute = [(1, 'ban', muc_ban, 2, L('Ban user.')),
	   (1, 'tban', muc_tempo_ban, 2, L('Temporary ban.\ntban show|del [jid] - show/del temporary bans\ntban nick\ntimeD|H|M|S\nreason - ban nick for time because reason.')),
	   (1, 'none', muc_none, 2, L('Delete user affiliation.')),
	   (1, 'member', muc_member, 2, L('Get member affiliation.')),
#	   (1, 'admin', muc_admin, 2, ''),
#	   (1, 'owner', muc_owner, 2, ''),
	   (1, 'afind', muc_afind, 2, L('Search in alist.')),
	   (1, 'kick', muc_kick, 2, L('Kick user.')),
	   (1, 'participant', muc_participant, 2, L('Give participant.')),
	   (1, 'visitor', muc_visitor, 2, L('Give visitor.')),
	   (1, 'moderator', muc_moderator, 2, L('Give role moderator.')),
	   (1, 'akick', muc_akick, 2, L('Autokick.\nakick show|del [jid] - show/del akick list\nakick nick\ntimeD|H|M|S\nreason - autokick nick for time because reason.')),
	   (1, 'aparticipant', muc_aparticipant, 2, L('Autoparticipant.\naparticipant show|del [jid] - show/del aparticipant list\naparticipant nick\ntimeD|H|M|S\nreason - give user participant affiliation for time because reason.')),
	   (1, 'avisitor', muc_avisitor, 2, L('Autovisitor.\navisitor show|del [jid] - show/del avisitor list\navisitor nick\ntimeD|H|M|S\nreason - autovisitor nick for time because reason.')),
	   (1, 'amoderator', muc_amoderator, 2, L('Automoderator.\namoderator show|del [jid] - show/del amoderator list\namoderator nick\ntimeD|H|M|S\nreason - auto give user role moderator for time because reason.')),
	   (1, 'global_ban', global_ban, 2, L('Global ban. Available only for confernce owner.\nglobal_ban del - remove conference from banlist,\nglobal_ban add - add conference into banlist,\nglobal_ban <jid> - ban jid in all rooms, where bot is admin.'))]
