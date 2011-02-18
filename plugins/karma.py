#!/usr/bin/python
# -*- coding: utf -*-

karmabasefile = os.path.isfile(karmabase)
karma_base = sqlite3.connect(karmabase,timeout=base_timeout)
cu_karmabase = karma_base.cursor()

if not karmabasefile:
	cu_karmabase.execute('''create table karma (room text, jid text, karma int)''')
	cu_karmabase.execute('''create table commiters (room text, jid text, karmajid text, last int)''')
	cu_karmabase.execute('''create index krj on karma (room,jid)''')
	cu_karmabase.execute('''create index crjk on karma (room,jid,karma)''')
	karma_base.commit()
karma_base.close()

def karma(type, jid, nick, text):
	arg = text.split(' ',1)
	try: arg1 = arg[1]
	except: arg1 = None
	a0l = arg[0].lower()

	karma_comm = {'show':		[karma_show,		(jid, nick, arg1)],
				  'top+':		[karma_top,			(jid, nick, arg1, None)],
				  'top-':		[karma_top,			(jid, nick, arg1, True)],
				  'set':		[karma_set,			(jid, nick, arg1)],
				  'clear':		[karma_clear,		(jid, nick, arg1)]}

	if karma_comm.has_key(a0l): msg = karma_comm[a0l][0](*karma_comm[a0l][1])
	else: msg = karma_show(jid, nick, text)
	send_msg(type, jid, nick, msg)
	
def karma_top(jid, nick, text, order):
	try: lim = int(text)
	except: lim = GT('karma_show_default_limit')
	if lim < 1: lim = 1
	elif lim > GT('karma_show_max_limit'): lim = GT('karma_show_max_limit')
	karma_base = sqlite3.connect(karmabase,timeout=base_timeout)
	cu_karmabase = karma_base.cursor()
	if order: stat = cu_karmabase.execute('select jid,karma from karma where room=? order by karma',(jid,)).fetchall()
	else: stat = cu_karmabase.execute('select jid,karma from karma where room=? order by -karma',(jid,)).fetchall()
	karma_base.close()
	if stat == None: return L('In this room karma is not changed!')
	msg, cnt = '', 1
	for tmp in stat:
		tmp2 = get_nick_by_jid(jid, tmp[0])
		if tmp2:
			msg += '\n'+str(cnt)+'. '+tmp2+'\t'+karma_val(int(tmp[1]))
			cnt += 1
		if cnt >= lim: break
	if len(msg): return L('Top karma: %s') % msg
	else: return L('Karma for members is present not changed!')

def karma_show(jid, nick, text):
	if text == None or text == '' or text == nick: text, atext = nick, L('Your')
	else: atext = text
	karmajid = getRoom(get_level(jid,text)[1])
	if karmajid == 'None': return L('I\'m not sure, but %s not is here.') % atext
	else:
		karma_base = sqlite3.connect(karmabase,timeout=base_timeout)
		cu_karmabase = karma_base.cursor()
		stat = cu_karmabase.execute('select karma from karma where room=? and jid=?',(jid,karmajid)).fetchone()
		karma_base.close()
		if stat == None: return L('%s have a clear karma') % atext
		else: return L('%s karma is %s') % (atext, karma_val(int(stat[0])))

def karma_set(jid, nick, text):
	cof = getFile(conoff,[])
	if (jid,'karma') in cof: return
	k_acc = get_level(jid,nick)[0]
	try:
		if text.count('\n'): text,val = text.split('\n',1)
		else: text,val = text.split(' ',1)	
		if k_acc >= 9:
			val = int(val)
			jid, karmajid = getRoom(jid), getRoom(get_level(jid,text)[1])
			if karmajid == getRoom(selfjid): return
			elif karmajid == 'None': return L('You can\'t change karma in outdoor conference!')
			else:
				karma_base = sqlite3.connect(karmabase,timeout=base_timeout)
				cu_karmabase = karma_base.cursor()
				cu_karmabase.execute('delete from karma where room=? and jid=?',(jid,karmajid)).fetchall()
				cu_karmabase.execute('insert into karma values (?,?,?)',(jid,karmajid,val)).fetchall()
				karma_base.commit()
				karma_base.close()
				val = karma_val(val)
				return L('You changes %s\'s karma to %s') % (text,val)
		else: return L('You can\'t change karma!')
	except: return L('incorrect digital parameter').capitalize()

def karma_clear(jid, nick, text):
	cof = getFile(conoff,[])
	if (jid,'karma') in cof: return
	k_acc = get_level(jid,nick)[0]
	if k_acc >= 9:
		jid, karmajid = getRoom(jid), getRoom(get_level(jid,text)[1])
		if karmajid == getRoom(selfjid): return
		elif karmajid == 'None': return L('You can\'t change karma in outdoor conference!')
		else:
			karma_base = sqlite3.connect(karmabase,timeout=base_timeout)
			cu_karmabase = karma_base.cursor()
			cu_karmabase.execute('delete from karma where room=? and jid=?',(jid,karmajid)).fetchall()
			karma_base.commit()
			karma_base.close()
			return L('You clear karma for %s') % text
	else: return L('You can\'t change karma!')

def karma_get_access(room,jid):
	karma_base = sqlite3.connect(karmabase,timeout=base_timeout)
	cu_karmabase = karma_base.cursor()
	stat = cu_karmabase.execute('select karma from karma where room=? and jid=?',(room,jid)).fetchone()
	karma_base.close()
	if stat == None: return None
	if int(stat[0]) < GT('karma_limit'): return None
	return True

def karma_val(val):
	if val == 0: return '0'
	elif val < 0: return str(val)
	else: return '+'+str(val)

def karma_correct(room):
	def karma_correct_diff(vm,ac):
		lim_up = [GT('karma_discret_lim_up')]
		lim_dn = [GT('karma_discret_lim_dn')]
		kd,rs = GT('karma_discret'),[]
		def validate_mass(m):
			for t in range(0,len(m)-1):
				if abs(m[t]-m[t+1]) < kd or m[t] >= m[t+1]: return False
			return True
		def karma_blur_mass(vm):
			vm = lim_dn + vm + lim_up
			nm = []
			for t in range(0,len(vm)-2): nm.append(int((vm[t]+vm[t+1]+vm[t+2])/3))
			return nm
		while not validate_mass(vm): vm = karma_blur_mass(vm)
		for t in range(0,len(ac)): rs.append([vm[t],ac[t]])
		return rs
	tm,ac,vm,nm = config_group_karma[2],[],[],[]
	for t in tm:
		df = re.findall(r'karma_action_[0-9](.*)',t)
		if df:
			ac += df
			try: tvm = int(get_config(room,t))
			except: tvm = int(config_prefs[t][3])
			vm.append(tvm)
			nm.append(t)
	vm = karma_correct_diff(vm,ac)
	for t in range(0,len(nm)): put_config(room,nm[t],str(vm[t][0]))
	return vm

def karma_action_do(room,text,action):
	tmppos = arr_semi_find(confbase, room)
	if tmppos == -1: nick = Settings['nickname']
	else: nick = getResourse(confbase[tmppos])
	act = {'outcast':muc_affiliation,'none':muc_affiliation,'member':muc_affiliation,
		   'kick':muc_role,'participant':muc_role,'visitor':muc_role,'moderator':muc_role}
	act[action]('chat',room,nick,'%s\n%s' % (text,get_config(room,'karma_action_reason')),action.replace('kick','none'),0)

def karma_change(room,jid,nick,type,text,value):
	if type == 'chat': msg = L('You can\'t change karma in private!')
	else:
		cof = getFile(conoff,[])
		if (room,'karma') in cof: return
		if text.count(': '): text = text.split(': ',1)[0]
		elif text.count(', '): text = text.split(', ',1)[0]
		else: return
		k_acc = get_level(room,nick)[0]
		if k_acc < 0: return
		if k_acc >= 4 or karma_get_access(room,getRoom(jid)):
			jid, karmajid = getRoom(jid), getRoom(get_level(room,text)[1])
			if karmajid == getRoom(selfjid): return
			elif karmajid == 'None': msg = L('You can\'t change karma in outdoor conference!')
			elif karmajid == jid: msg = L('You can\'t change own karma!')
			else:
				karma_base = sqlite3.connect(karmabase,timeout=base_timeout)
				cu_karmabase = karma_base.cursor()
				stat = cu_karmabase.execute('select last from commiters where room=? and jid=? and karmajid=?',(room,jid,karmajid)).fetchone()
				karma_valid, karma_time = None, int(time.time())
				if stat == None: karma_valid = True
				elif karma_time - int(stat[0]) >= GT('karma_timeout')[k_acc]: karma_valid = True
				if karma_valid:
					if stat: cu_karmabase.execute('update commiters set last=? where room=? and jid=? and karmajid=?',(karma_time,room,jid,karmajid))
					else: cu_karmabase.execute('insert into commiters values (?,?,?,?)',(room,jid,karmajid,karma_time))
					stat = cu_karmabase.execute('select karma from karma where room=? and jid=?',(room,karmajid)).fetchone()
					if stat:
						stat = stat[0]+value
						cu_karmabase.execute('delete from karma where room=? and jid=?',(room,karmajid)).fetchall()
					else: stat = value
					cu_karmabase.execute('insert into karma values (?,?,?)',(room,karmajid,stat)).fetchall()
					msg = L('You changes %s\'s karma to %s. Next time to change across: %s.') % (text,karma_val(stat),un_unix(GT('karma_timeout')[k_acc]))
					karma_base.commit()
					pprint('karma change in %s for %s to %s' % (room,text,stat))
					am = None
					if get_config(room,'karma_action'):
						kmass = karma_correct(room)
						for t in kmass:
							if t[0] <= 0 and stat <= t[0]:
								am = (room,text,t[1])
								break
							elif t[0] > 0 and stat >= t[0]: am = (room,text,t[1])
						if am:
							karma_action_do(*am)
							pprint('karma action in %s for %s is %s' % am)
				else: msg = L('Time from last change %s\'s karma is very small. Please wait %s.') % (text,un_unix(int(stat[0])+GT('karma_timeout')[k_acc]-karma_time))
				karma_base.close()
		else: msg = L('You can\'t change karma!')
	send_msg(type, room, nick, msg)

def karma_check(room,jid,nick,type,text):
	if getRoom(jid) == getRoom(selfjid): return
	if len(unicode(text)) < 5: return
	while len(text) and text[-1:] == ' ': text = text[:-1]
	if text[-3:] == ' +1':
		karma_change(room,jid,nick,type,text,1)
		return True
	elif text[-3:] == ' -1':
		karma_change(room,jid,nick,type,text,-1)
		return True

global execute, message_control

message_act_control = [karma_check]

execute = [(3, 'karma', karma, 2, L('Karma.\nkarma [show] nick\nkarma top+|- [count]\nFor change karma: nick: +1\nnick: -1'))]
