#!/usr/bin/python
# -*- coding: utf -*-

# acl [del] /time show|msg|message|prs|presence|nick|jid|all sub|exp .*|some command

# acl = jid,action,type,text,command

acl_help = '''Actions list.
acl show - show list
acl del item - remove item from list
acl [/time] msg|message|prs|presence|nick|jid|all [sub|exp|cexp] pattern command - execute command by condition
allowed variables in commands: ${NICK}, ${JID}
sub = substring, exp = regular expression, cexp = case sensitive regular expression
time format is /number+identificator. s = sec, m = min, d = day, w = week, M = month, y = year. only one identificator allowed!'''

acl_acts = ['msg','message','prs','presence','nick','jid','all']
acl_actions = ['show','del'] + acl_acts

acl_base = set_folder+'acl.db'

def open_acl_base():
	is_acl = os.path.isfile(acl_base)
	aclb = sqlite3.connect(acl_base)
	acur = aclb.cursor()
	if not is_acl:
		acur.execute('create table acl (jid text, action text, type text, text text, command text, time int)')
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
			if tmp[5]: st,tp = '\n[%s] %s %s %s %s', (time.ctime(float(tmp[5])),) + tmp[1:4] + (tmp[4].replace('\n',' // '),)
			else: st,tp = '\n%s %s %s %s', tmp[1:4] + (tmp[4].replace('\n',' // '),)
			msg += st % tp
	else: msg = L('Acl not found')
	return msg

def acl_add_del(jid,text,flag):
	time_mass,atime = {'s':1,'m':60,'h':3600,'d':86400,'w':604800,'M':2592000,'y':31536000},0
	if text[0][0] == '/':
		try: atime = int(time.time()) + int(text[0][1:-1]) * time_mass[text[0][-1:]]
		except: pass
		text = text[1:]
	acl_cmd = text[0].lower()
	text = text[1:]
	if not acl_cmd in acl_acts: msg = L('Items: %s') % '|'.join(acl_acts)
	else:
		#sub|exp .*|some visitor|kick|ban|participant|member|none|say
		if text[0].lower() in ['sub','exp','cexp','=']: acl_sub_act,text = text[0].lower(),text[1:]
		else: acl_sub_act = '='
		text[0] = text[0].replace('%20','\ ')
		if acl_sub_act in ['exp','cexp']:
			try: re.compile(text[0])
			except: return L('Error in RegExp!')	
		aclb,acur = open_acl_base()
		tmp = acur.execute('select * from acl where jid=? and action=? and type=? and text=?',(jid,acl_cmd, acl_sub_act, text[0])).fetchall()
		if tmp:
			acur.execute('delete from acl where jid=? and action=? and type=? and text=?',(jid,acl_cmd, acl_sub_act, text[0])).fetchall()
			msg = [L('Removed:'),L('Updated:')][flag]
		else: msg = [L('Not found:'),L('Added:')][flag]
		if flag: acur.execute('insert into acl values (?,?,?,?,?,?)', (jid, acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ '), atime))
		close_acl_base(aclb)			
		if atime: msg += ' [%s] %s %s %s %s' % (time.ctime(atime),acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ ').replace('\n',' // '))
		else: msg += ' %s %s %s %s' % (acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ ').replace('\n',' // '))
	return msg

def acl_add(jid,text): return acl_add_del(jid,text,True)

def acl_del(jid,text): return acl_add_del(jid,text,False)
	
	
def muc_acl(type, jid, nick, text):
	text = text.replace('\ ','%20').split(' ')
	while text.count(''): text.remove('')
	acl_cmd = text[0].lower()
	if not acl_cmd in acl_actions and acl_cmd[0] != '/': msg = L('Items: %s') % '|'.join(acl_actions)
	elif acl_cmd == 'show': msg = acl_show(jid)
	elif acl_cmd == 'del': msg = acl_del(jid,text[1:])
	else: msg = acl_add(jid,text)
	send_msg(type, jid, nick, msg)

def acl_action(cmd,nick,jid,room):
	global last_command
	if len(last_command): 
		if last_command[6] == Settings['jid']: last_command = []
	cmd = cmd.replace('${NICK}',nick).replace('${JID}',jid)
	tmppos = arr_semi_find(confbase, room)
	if tmppos == -1: nowname = nickname
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '': nowname = nickname
	com_parser(7, nowname, 'groupcat', room, nick, cmd, Settings['jid'])
	
def acl_message(room,jid,nick,type,text):
	if not no_comm: return
	if get_level(room,nick)[0] < 0: return
	if getRoom(jid) == getRoom(Settings['jid']): return
	aclb,acur = open_acl_base()
	a = acur.execute('select action,type,text,command,time from acl where jid=? and (action=? or action=? or action=?)',(room,'msg','message','all')).fetchall()
	if a:
		for tmp in a:
			if tmp[4] <= time.time() and tmp[4]: acur.execute('delete from acl where jid=? and action=? and type=? and text=?',(room,tmp[0],tmp[1],tmp[2])).fetchall()
			if tmp[1] == 'exp' and re.match(tmp[2],text,re.I+re.S+re.U):
				acl_action(tmp[3],nick,jid,room)
				break
			elif tmp[1] == 'cexp' and re.match(tmp[2],text,re.S+re.U):
				acl_action(tmp[3],nick,jid,room)
				break
			elif tmp[1] == 'sub' and text.lower().count(tmp[2].lower()):
				acl_action(tmp[3],nick,jid,room)
				break
			elif text.lower() == tmp[2].lower():
				acl_action(tmp[3],nick,jid,room)
				break
	close_acl_base(aclb)			

def acl_presence(room,jid,nick,type,mass):
	if get_level(room,nick)[0] < 0: return
	if getRoom(jid) == getRoom(Settings['jid']): return
	aclb,acur = open_acl_base()
	a = acur.execute('select action,type,text,command,time from acl where jid=? and (action=? or action=? or action=? or action=? or action=?)',(room,'prs','presence','nick','jid','all')).fetchall()
	if a:
		for tmp in a:
			if tmp[4] <= time.time() and tmp[4]: acur.execute('delete from acl where jid=? and action=? and type=? and text=?',(room,tmp[0],tmp[1],tmp[2])).fetchall()
			if tmp[0] in ['presence','prs']: itm = mass[0]
			elif tmp[0] == 'nick': itm = nick
			elif tmp[0] == 'jid': itm = jid
			elif tmp[0] == 'all': itm = jid+nick+mass[0]
			if tmp[1] == 'exp' and re.match(tmp[2],itm,re.I+re.S+re.U):
				acl_action(tmp[3],nick,jid,room)
				break
			elif tmp[1] == 'cexp' and re.match(tmp[2],itm,re.S+re.U):
				acl_action(tmp[3],nick,jid,room)
				break
			elif tmp[1] == 'sub' and itm.lower().count(tmp[2].lower()):
				acl_action(tmp[3],nick,jid,room)
				break
			elif itm.lower() == tmp[2].lower() or (tmp[0] == 'all' and tmp[2].lower() in (jid.lower(),nick.lower(),mass[0].lower())):
				acl_action(tmp[3],nick,jid,room)
				break
	close_acl_base(aclb)				
global execute, presence_control, message_control

presence_control = [acl_presence]
message_control = [acl_message]

execute = [(7, 'acl', muc_acl, 2, L(acl_help))]
