#!/usr/bin/python
# -*- coding: utf -*-

acl_acts = ['msg','message','prs','presence','role','affiliation','nick','jid','jidfull','res','all','age','ver','version']
acl_actions = ['show','del'] + acl_acts

acl_base = set_folder+'acl.db'

acl_ver_tmp = {}

def open_acl_base():
	is_acl = os.path.isfile(acl_base)
	aclb = sqlite3.connect(acl_base,timeout=base_timeout)
	acur = aclb.cursor()
	if not is_acl: acur.execute('create table acl (jid text, action text, type text, text text, command text, time int)')
	return aclb,acur

def close_acl_base(base):
	base.commit()
	base.close()

def acl_show(jid):
	aclb,acur = open_acl_base()
	a = acur.execute('select * from acl where jid=?',(jid,)).fetchall()
	close_acl_base(aclb)
	if len(a):
		msg = L('Acl:')
		for tmp in a:
			if tmp[5]: st,tp = '\n[%s] %s %s %s -> %s', (time.ctime(float(tmp[5])),) + tmp[1:4] + (tmp[4].replace('\n',' // '),)
			else: st,tp = '\n%s %s %s -> %s', tmp[1:4] + (tmp[4].replace('\n',' // '),)
			msg += st % tp
	else: msg = L('Acl not found')
	return msg

def acl_add_del(jid,text,flag):
	time_mass,atime = {'s':1,'m':60,'h':3600,'d':86400,'w':604800,'M':2592000,'y':31536000},0
	silent = False
	try:
		while text[0][0] == '/':
			if text[0] == '/silent': silent = True
			else:
				try: atime = int(time.time()) + int(text[0][1:-1]) * time_mass[text[0][-1:]]
				except: return L('Time format error!')
			text = text[1:]
	except: return L('Error in parameters. Read the help about command.')
	ttext = ' '.join(text)
	if operator.xor(ttext.count('${EXP}') <= 1,ttext.count('${/EXP}') <= 1) and flag: return L('Error in parameters. Read the help about command.')
	elif ttext.find('${EXP}',ttext.find('${/EXP}')) > 0 and flag: return L('Error in parameters. Read the help about command.')
	elif ttext.count('${EXP}') and ttext.count('${/EXP}'):
		try: re.compile(ttext.split('${EXP}',1)[1].split('${/EXP}',1)[0].replace('%20','\ ').replace('*','*?'))
		except: return L('Error in RegExp!')	
	acl_cmd = text[0].lower()
	text = text[1:]
	if not acl_cmd in acl_acts: msg = L('Items: %s') % '|'.join(acl_acts)
	else:
		try:
			if text[0].lower() in ['sub','exp','cexp','=','<','>','<=','>=']: acl_sub_act,text = text[0].lower(),text[1:]
			else: acl_sub_act = '='
		except: return L('Error in parameters. Read the help about command.')
		if acl_cmd != 'age' and acl_sub_act in ['<','>','<=','>=']: return L('Error in parameters. Read the help about command.')		
		if acl_sub_act in ['=','sub']: text[0] = text[0].replace('%20',' ')
		else: text[0] = text[0].replace('%20','\ ')
		if acl_sub_act in ['exp','cexp']:
			try: re.compile(text[0].replace('*','*?'))
			except: return L('Error in RegExp!')	
		aclb,acur = open_acl_base()
		tmp = acur.execute('select * from acl where jid=? and action=? and type=? and text=?',(jid,acl_cmd, acl_sub_act, text[0])).fetchall()
		if tmp:
			acur.execute('delete from acl where jid=? and action=? and type=? and text=?',(jid,acl_cmd, acl_sub_act, text[0])).fetchall()
			msg = [L('Removed:'),L('Updated:')][flag]
		else: msg = [L('Not found:'),L('Added:')][flag]
		if flag: acur.execute('insert into acl values (?,?,?,?,?,?)', (jid, acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ '), atime))
		close_acl_base(aclb)			
		if atime: msg += ' [%s] %s %s %s -> %s' % (time.ctime(atime),acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ ').replace('\n',' // '))
		else: msg += ' %s %s %s -> %s' % (acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ ').replace('\n',' // '))
	if silent: return L('done')
	else: return msg

def acl_add(jid,text): return acl_add_del(jid,text,True)

def acl_del(jid,text): return acl_add_del(jid,text,False)

def muc_acl(type, jid, nick, text):
	text = text.replace('\ ','%20').split(' ')
	while text.count(''): text.remove('')
	if len(text): acl_cmd = text[0].lower()
	else: acl_cmd = '!'
	if not acl_cmd in acl_actions and acl_cmd[0] != '/': msg = L('Items: %s') % '|'.join(acl_actions)
	elif acl_cmd == 'show': msg = acl_show(jid)
	elif acl_cmd == 'del': msg = acl_del(jid,text[1:])
	else: msg = acl_add(jid,text)
	send_msg(type, jid, nick, msg)

def acl_action(cmd,nick,jid,room,text):
	global last_command
	if len(last_command): 
		if last_command[6] == Settings['jid']: last_command = []
	cmd = cmd.replace('${NICK}',nick).replace('${JID}',jid).replace('${SERVER}',getServer(jid))
	if text and '${EXP}' in cmd and '${/EXP}' in cmd:
		regex = cmd.split('${EXP}',1)[1].split('${/EXP}',1)[0]
		mt = re.findall(regex, text, re.S+re.U+re.I)
		if mt != []: txt = ''.join(mt[0])
		else: txt = ''
		cmd = cmd.split('${EXP}',1)[0] + txt + cmd.split('${/EXP}',1)[1]
	tmppos = arr_semi_find(confbase, room)
	if tmppos == -1: nowname = Settings['nickname']
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '': nowname = Settings['nickname']
	return com_parser(7, nowname, 'groupchat', room, nick, cmd, Settings['jid'])
	
def acl_message(room,jid,nick,type,text):
	#if not no_comm: return
	if get_level(room,nick)[0] < 0: return
	if getRoom(jid) == getRoom(Settings['jid']): return
	aclb,acur = open_acl_base()
	a = acur.execute('select action,type,text,command,time from acl where jid=? and (action=? or action=? or action=?)',(room,'msg','message','all')).fetchall()
	no_comm = True
	if a:
		for tmp in a:
			if tmp[4] <= time.time() and tmp[4]: acur.execute('delete from acl where jid=? and action=? and type=? and text=?',(room,tmp[0],tmp[1],tmp[2])).fetchall()
			if tmp[1] == 'exp' and re.match(tmp[2].replace('*','*?'),text,re.I+re.S+re.U):
				no_comm = acl_action(tmp[3],nick,jid,room,text)
				break
			elif tmp[1] == 'cexp' and re.match(tmp[2].replace('*','*?'),text,re.S+re.U):
				no_comm = acl_action(tmp[3],nick,jid,room,text)
				break
			elif tmp[1] == 'sub' and text.lower().count(tmp[2].lower()):
				no_comm = acl_action(tmp[3],nick,jid,room,text)
				break
			elif text.lower() == tmp[2].lower():
				no_comm = acl_action(tmp[3],nick,jid,room,text)
				break
	close_acl_base(aclb)
	return not no_comm

def acl_presence(room,jid,nick,type,mass):
	global iq_request,acl_ver_tmp
	#if get_level(room,nick)[0] < 0: return
	if getRoom(jid) == getRoom(Settings['jid']): return
	was_joined = not mass[7] or is_start
	if type == 'unavailable':
		try: acl_ver_tmp.pop('%s/%s' % (room,nick))
		except: pass
		return
	# actions only on joins
	# if was_joined: return
	aclb,acur = open_acl_base()
	a = acur.execute('select action,type,text,command,time from acl where jid=? and (action=? or action=? or action=? or action=? or action=? or action=? or action=? or action=? or action=? or action=? or action=?)',(room,'prs','presence','nick','jid','jidfull','res','all','role','affiliation','age','ver')).fetchall()
	if a:
		for tmp in a:
			if tmp[0] == 'age':
				mdb = sqlite3.connect(agestatbase,timeout=base_timeout)
				cu = mdb.cursor()
				in_base = cu.execute('select time,sum(age),status from age where room=? and jid=? order by status',(room,getRoom(jid))).fetchall()
				mdb.close()
				if not in_base: r_age = 0
				else:
					try:
						tm = in_base[0]
						if tm[2]: r_age = tm[1]
						else: r_age = int(time.time())-tm[0]+tm[1]
					except: r_age = 0
				break
				
		for tmp in a:
			if tmp[0] == 'ver' and was_joined:
				try: r_ver = acl_ver_tmp['%s/%s' % (room,nick)]
				except:
					iqid,who = get_id(), '%s/%s' % (room,nick)
					i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_VERSION},[])])
					iq_request[iqid]=(time.time(),acl_version_async,[a, nick, jid, room, mass[0]])
					sender(i)
					r_ver = None
					pprint('*** ACL version request for %s/%s' % (room,nick))
					break

		for tmp in a:
			if tmp[4] <= time.time() and tmp[4]: acur.execute('delete from acl where jid=? and action=? and type=? and text=?',(room,tmp[0],tmp[1],tmp[2])).fetchall()
			if tmp[0] in ['presence','prs']: itm = mass[0]
			elif tmp[0] == 'nick': itm = nick
			elif tmp[0] == 'jid': itm = getRoom(jid)
			elif tmp[0] == 'jidfull': itm = jid
			elif tmp[0] == 'res': itm = getResourse(jid)
			elif tmp[0] == 'role': itm = mass[1]
			elif tmp[0] == 'affiliation': itm = mass[2]
			elif tmp[0] == 'all': itm = jid+nick+mass[0]+mass[1]+mass[2]
			elif tmp[0] == 'ver':
				if was_joined and r_ver: itm = r_ver
				else: itm = ''
			elif tmp[0] == 'age':
				if eval('%s%s%s' % (r_age,tmp[1],tmp[2])):
					acl_action(tmp[3],nick,jid,room,None)
					break
				else: itm = ''
			if tmp[1] == 'exp' and re.match(tmp[2].replace('*','*?'),itm,re.I+re.S+re.U):
				acl_action(tmp[3],nick,jid,room,None)
				break
			elif tmp[1] == 'cexp' and re.match(tmp[2].replace('*','*?'),itm,re.S+re.U):
				acl_action(tmp[3],nick,jid,room,None)
				break
			elif tmp[1] == 'sub' and itm.lower().count(tmp[2].lower()):
				acl_action(tmp[3],nick,jid,room,None)
				break
			elif itm.lower() == tmp[2].lower() or (tmp[0] == 'all' and tmp[2].lower() in (jid.lower(),nick.lower(),mass[0].lower())):
				acl_action(tmp[3],nick,jid,room,None)
				break
	close_acl_base(aclb)

def acl_version_async(a, nick, jid, room, mass, is_answ):
	global acl_ver_tmp
	isa = is_answ[1]
	if len(isa) == 3: itm = '%s %s // %s' % isa
	else: itm = ' '.join(isa)
	acl_ver_tmp['%s/%s' % (room,nick)] = itm
	for tmp in a:
		if tmp[0] == 'ver':
			if tmp[1] == 'exp' and re.match(tmp[2].replace('*','*?'),itm,re.I+re.S+re.U): acl_action(tmp[3],nick,jid,room,None)
			elif tmp[1] == 'cexp' and re.match(tmp[2].replace('*','*?'),itm,re.S+re.U): acl_action(tmp[3],nick,jid,room,None)
			elif tmp[1] == 'sub' and itm.lower().count(tmp[2].lower()): acl_action(tmp[3],nick,jid,room,None)
			elif itm.lower() == tmp[2].lower() or (tmp[0] == 'all' and tmp[2].lower() in (jid.lower(),nick.lower(),mass.lower())): acl_action(tmp[3],nick,jid,room,None)

global execute, presence_control, message_act_control

presence_control = [acl_presence]
message_act_control = [acl_message]

execute = [(7, 'acl', muc_acl, 2, L('Actions list.\nacl show - show list\nacl del [/silent] item - remove item from list\nacl [/time] [/silent] msg|message|prs|presence|role|affiliation|nick|jid|jidfull|res|all [sub|exp|cexp] pattern command - execute command by condition\nallowed variables in commands: ${NICK}, ${JID}, ${SERVER}\nsub = substring, exp = regular expression, cexp = case sensitive regular expression\ntime format is /number+identificator. s = sec, m = min, d = day, w = week, M = month, y = year. only one identificator allowed!'))]
