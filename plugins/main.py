# -*- coding: utf-8 -*-

def shell_execute(cmd):
	sys.exc_clear()
	gc.collect()
	bufsize = 1024
	p = Popen(cmd, shell=True, bufsize=bufsize, stdout=PIPE, stderr=STDOUT, close_fds=True)
	return ''.join(map(lambda x: x.decode('utf-8'), p.stdout.readlines()))

def concat(list):
	result = ''
	for tmp in list: result += tmp
	return result

def get_affiliation(jid,nick):
	xtype = ''
	for base in megabase:
		if base[0].lower() == jid and base[1] == nick:
			xtype = base[3]
			break
	return xtype

def comm_on_off(type, jid, nick, text):
	cof = getFile(conoff,[])
	if len(text):
		if text[:3] == 'on ':
			text = text[3:].lower()
			if len(text):
				if cof.count((jid,text)):
					if get_affiliation(jid,nick) == 'owner' or get_access(jid,nick)[0] == 2:
						cof.remove((jid,text))
						writefile(conoff, str(cof))
						msg = u'Включено: '+text
					else: msg = u'Включение команд доступно только владельцу конференции'
				else: msg = u'Для данной конференции команда '+text+u' не была отключена!'
			else: msg = u'Что включить?'
		if text[:4] == 'off ':
			if get_affiliation(jid,nick) == 'owner' or get_access(jid,nick)[0] == 2:
				text = text[4:].lower()
				if len(text):
					text = text.split(' ')
					msg_found = ''
					msg_notfound = ''
					msg_offed = ''
					for tex in text:
						fl = 0
						if tex != 'comm':
							for cm in comms:
								if cm[1] == tex:
									fl = 1
									break
						if fl:
							if not cof.count((jid,tex)):
								cof.append((jid,tex))
								writefile(conoff, str(cof))
								msg_found += tex + ', '
							else: msg_offed += tex + ', '
						else: msg_notfound += tex + ', '
					if len(msg_found): msg = u'Отключены команды: '+msg_found[:-2]
					else: msg = u''
					if len(msg_offed):
						if msg != '': msg += '\n'
						msg += u'Отключенные ранее команды: '+msg_offed[:-2]
					if len(msg_notfound):
						if msg != '': msg += '\n'
						msg += u'Не найдены команды: '+msg_notfound[:-2]
				else: msg = u'Что отключить?'
			else: msg = u'Отключение команд доступно только владельцу конференции'
	else:
		msg = ''
		for tmp in cof:
			if tmp[0] == jid: msg += tmp[1] + u', '
		if len(msg): msg = u'Отключены команды: ' + msg[:-2]
		else: msg = u'Для данной конференции нет отключенных команд'
	send_msg(type, jid, nick, msg)

def reduce_spaces(text):
	while text[0] == ' ': text = text[1:]
	while text[-1:] == ' ': text = text[:-1]
	return text

def censor_status(type, jid, nick, text):
	tmode = 0
	if text:
		if text.lower() == 'on': tmode = 2
		elif text.lower() == 'off': tmode = 1

	gl_censor = getFile(cns,[(getRoom(jid),0)])
	msg = u'Censor is '
	is_found = 1
	for sm in gl_censor:
		if sm[0] == getRoom(jid):
			if tmode: tsm = (sm[0],tmode-1)
			else: tsm = (sm[0],int(not sm[1]))
			gl_censor.remove(sm)
			gl_censor.append(tsm)
			is_found = 0
			ssta = tsm[1]
	if is_found:
		gl_censor.append((getRoom(jid),1))
		ssta = 1
	msg += onoff(ssta)
	writefile(cns,str(gl_censor))
	send_msg(type, jid, nick, msg)

def status(type, jid, nick, text):
	if text == '': text = nick
	mdb = sqlite3.connect(agestatbase)
	cu = mdb.cursor()
	stat = cu.execute('select message,status from age where nick=? and room=?',(text,jid)).fetchone()
	stat2 = cu.execute('select message,status from age where jid=? and room=?',('<temporary>'+text.lower()+'@',jid)).fetchone()
	if stat2: stat = stat2
	if stat:
		if stat[1]: msg = u'покинул данную конференцию.'
		else:
			stat = stat[0].split('\n',4)
			if stat[3] != 'None': msg = stat[3]
			else: msg = 'online'
			if stat[4] != 'None': msg += ' ('+stat[4]+')'
			if stat[2] != 'None': msg += ' ['+stat[2]+'] '
			else: msg += ' [0] '
			if stat[0] != 'None' and stat[1] != 'None': msg += stat[0]+'/'+stat[1]
		if text != nick: msg = text + ' - '+msg
	else: msg = u'Не найдено!'
	send_msg(type, jid, nick, msg)

def replacer(msg):
	msg = rss_replace(msg)
	msg = rss_del_html(msg)
	msg = rss_replace(msg)
	msg = rss_del_nn(msg)
	return msg

def svn_info(type, jid, nick):
	if os.path.isfile(ul): msg = u'Последнее обновление:\n'+readfile(ul).decode('utf-8')
	else: msg = u'Файл '+ul+u' не доступен!'
	send_msg(type, jid, nick, msg)

def unhtml(page):
	for a in range(0,page.count('<style')):
		ttag = get_tag_full(page,'style')
		page = page.replace(ttag,'')

	for a in range(0,page.count('<script')):
		ttag = get_tag_full(page,'script')
		page = page.replace(ttag,'')

	page = rss_replace(page)
	page = rss_repl_html(page)
	page = rss_replace(page)
	page = rss_del_nn(page)
	page = page.replace('\n ','')
	return page

def alias(type, jid, nick, text):
	global aliases
	aliases = getFile(alfile,[])
	gs = text.find(' ')
	if gs >= 0:
		mode = text[:gs]
		text = text[gs+1:]
		gs = text.find('=')
		if gs >= 0:
			cmd = text[:gs]
			cbody = text[gs+1:]
		else:
			cmd = text
			cbody = ''
	else:
		mode = text
		cmd = ''
		cbody = ''
	msg = u'Режим '+mode+u' не опознан!'
	if mode=='add':
		fl = 0
		for i in aliases:
			if i[1] == cmd and i[0] == jid:
				aliases.remove(i)
				fl = 1	
		aliases.append([jid, cmd, cbody])
		if fl: msg = u'Обновлено:'
		else: msg = u'Добавлено:'
		msg += u' '+cmd+u' == '+cbody
	if mode=='del':
		msg = u'Не возможно удалить '+cmd
		for i in aliases:
			if i[1] == cmd and i[0] == jid:
				aliases.remove(i)
				msg = u'Удалено: '+cmd
	if mode=='show':
		if cmd == '':
			msg = u'Сокращения: '
			isf = 1
			for i in aliases:
				if i[0] == jid:
					msg += i[1] + ', '
					isf = 0
			if isf: msg+=u'не найдены'
			else: msg = msg[:-2]
		else:
			msg = cmd
			isf = 1
			for i in aliases:
				if i[1].lower().count(cmd.lower()) and i[0] == jid:
					msg += '\n'+i[1]+' = '+i[2]
					isf = 0
			if isf: msg+=u' не найдено'
	writefile(alfile,str(aliases))
	send_msg(type, jid, nick, msg)

def fspace(mass):
	bdd = []
	for b in mass:
		if len(b) and len(b) != b.count(' '):
			while b[0] == ' ': b = b[1:]
		bdd.append(b)
	return bdd

def autoflood(type, jid, nick, text):
	tmode = 0
	if text:
		if text.lower() == 'on': tmode = 2
		elif text.lower() == 'off': tmode = 1

	floods = getFile(fld,[(getRoom(jid),0)])
	msg = u'Flood is '
	is_found = 1
	for sm in floods:
		if sm[0] == getRoom(jid):
			if tmode: tsm = (sm[0],tmode-1)
			else: tsm = (sm[0],int(not sm[1]))
			floods.remove(sm)
			floods.append(tsm)
			is_found = 0
			ssta = tsm[1]
	if is_found:
		floods.append((getRoom(jid),1))
		ssta = 1
	msg += onoff(ssta)
	writefile(fld,str(floods))
	send_msg(type, jid, nick, msg)

def del_space_begin(text):
	if len(text):
		while text[:1] == ' ': text = text[1:]
	return text

def del_space_end(text):
	if len(text):
		while text[-1:] == ' ': text = text[:-1]
	return text

def un_unix(val):
	tsec = int(val)-int(val/60)*60
	val = int(val/60)
	tmin = int(val)-int(val/60)*60
	val = int(val/60)
	thour = int(val)-int(val/24)*24
	tday = int(val/24)
	ret = tZ(thour)+':'+tZ(tmin)+':'+tZ(tsec)
	if tday: ret = str(tday)+' day(s) '+ret
	return ret

def close_age_null():
	mdb = sqlite3.connect(agestatbase)
	cu = mdb.cursor()
	cu.execute('delete from age where jid like ?',('<temporary>%',)).fetchall()
	ccu = cu.execute('select * from age where status=? order by room',(0,)).fetchall()
	cu.execute('delete from age where status=?', (0,)).fetchall()
	for ab in ccu: cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (ab[0],ab[1],ab[2],ab[3],ab[4],1,ab[6],ab[7]))
	mdb.commit()

def close_age():
	mdb = sqlite3.connect(agestatbase)
	cu = mdb.cursor()
	cu.execute('delete from age where jid like ?',('<temporary>%',)).fetchall()
	ccu = cu.execute('select * from age where status=? order by room',(0,)).fetchall()
	cu.execute('delete from age where status=?', (0,)).fetchall()
	tt = int(time.time())
	for ab in ccu: cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (ab[0],ab[1],ab[2],tt,ab[4]+(tt-ab[3]),1,ab[6],ab[7]))
	mdb.commit()

def close_age_room(room):
	mdb = sqlite3.connect(agestatbase)
	cu = mdb.cursor()
	cu.execute('delete from age where jid like ?',('<temporary>%',)).fetchall()
	ccu = cu.execute('select * from age where status=? and room=? order by room',(0,room)).fetchall()
	cu.execute('delete from age where status=? and room=?',(0,room)).fetchall()
	tt = int(time.time())
	for ab in ccu: cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (ab[0],ab[1],ab[2],tt,ab[4]+(tt-ab[3]),1,ab[6],ab[7]))
	mdb.commit()

def sfind(mass,stri):
	for a in mass:
		if a.count(stri): return a
	return ''

def get_local_prefix(jid):
	lprefix = prefix
	if os.path.isfile(preffile):
		pref = eval(readfile(preffile))
		for pp in pref:
			if pp[0] == getRoom(jid):
				lprefix = pp[1]
				break
	return lprefix

def get_prefix(prefix):
	if prefix != u'': return prefix
	else: return u'отсутствует'

def set_prefix(type, jid, nick, text):
	global preffile, prefix
	msg = u'Префикс команд: '

	if text != '': lprefix = text
	if text.lower() == 'none': lprefix = u''
	if text.lower() == 'del': lprefix = prefix

	if len(text):
		if os.path.isfile(preffile):
			pref = eval(readfile(preffile))
			for pp in pref:
				if pp[0] == getRoom(jid):
					pref.remove(pp)
					break
			pref.append((getRoom(jid),lprefix))
			writefile(preffile,str(pref))
		else:
			pref = [(getRoom(jid),lprefix)]
			writefile(preffile,str(pref))
	else: lprefix = get_local_prefix(jid)
	msg += get_prefix(lprefix)
	send_msg(type, jid, nick, msg)

def smile(type, jid, nick, text):
	tmode = 0
	if text:
		if text.lower() == 'on': tmode = 2
		elif text.lower() == 'off': tmode = 1
	smiles = getFile(sml,[(getRoom(jid),0)])
	msg = u'Smiles is '
	is_found = 1
	for sm in smiles:
		if sm[0] == getRoom(jid):
			if tmode: tsm = (sm[0],tmode-1)
			else: tsm = (sm[0],int(not sm[1]))
			smiles.remove(sm)
			smiles.append(tsm)
			is_found = 0
			ssta = tsm[1]
	if is_found:
		smiles.append((getRoom(jid),1))
		ssta = 1
	msg += onoff(ssta)
	writefile(sml,str(smiles))
	send_msg(type, jid, nick, msg)

def uptime(type, jid, nick):
	msg = u'Время работы: ' + get_uptime_str()+ u', Последняя сессия: '+un_unix(int(time.time())-sesstime)
	send_msg(type, jid, nick, msg)

def show_error(type, jid, nick, text):
	if text.lower() == 'clear': writefile(LOG_FILENAME,'')
	try: cmd = int(text)
	except: cmd = 1

	if os.path.isfile(LOG_FILENAME) and text.lower() != 'clear':
		log = str(readfile(LOG_FILENAME))
		log = log.split('ERROR:')

		lll = len(log)
		if cmd > lll: cmd = lll
		
		msg = u'Total Error(s): '+str(lll-1)+'\n'
		if text != '':
			for aa in range(lll-cmd,lll): msg += log[aa]+'\n'
		else: msg += ' '
		msg = msg[:-2]
	else: msg = u'No Errors'
	send_msg(type, jid, nick, msg)

def get_access(cjid, cnick):
	access_mode = -2
	jid = 'None'
	for base in megabase:
		if base[1].count(cnick) and base[0].lower()==cjid:
			jid = base[4]
			if base[3]==u'admin' or base[3]==u'owner':
				access_mode = 1
				break
			if base[3]==u'member' or base[3]==u'none':
				access_mode = 0
				break
	for iib in ignorebase:
		grj = getRoom(jid.lower())
		if iib.lower() == grj:
			access_mode = -1
			break
		if not (iib.count('.')+iib.count('@')) and grj.count(iib.lower()):
			access_mode = -1
			break
	if ownerbase.count(getRoom(jid)): access_mode = 2
	if jid == 'None' and ownerbase.count(getRoom(cjid)): access_mode = 2
	return (access_mode, jid)

def info_whois(type, jid, nick, text):
	if text != '': msg = raw_who(jid, text)
	else: msg = u'Кто нужен?'
	send_msg(type, jid, nick, msg)
		
def info_access(type, jid, nick):
	msg = raw_who(jid, nick)
	send_msg(type, jid, nick, msg)

def raw_who(room,nick):
	ta = get_access(room,nick)
	access_mode = ta[0]
	if access_mode == -2: msg = u'А был ли мальчег?'
	else:
		realjid = ta[1]
		msg = u'Доступ: '+str(access_mode)
		tb = [u'Игнорируемый',u'Минимальный',u'Админ/Владелец конфы',u'Владелец бота']
		msg += ', ' + tb[access_mode+1]
		if realjid != 'None': msg += u', jid опознан'
		msg += u', Префикс: ' + get_prefix(get_local_prefix(room))
	return msg

def info_comm(type, jid, nick):
	global comms
	msg = ''
	ta = get_access(jid,nick)
	access_mode = ta[0]
	tmp = sqlite3.connect(':memory:')
	cu = tmp.cursor()
	cu.execute('''create table tempo (comm text, am integer)''')
	for i in comms:
		if access_mode >= i[0]: cu.execute('insert into tempo values (?,?)', (unicode(i[1]),i[0]))
	for j in range(0,access_mode+1):
		cm = cu.execute('select * from tempo where am=? order by comm',(j,)).fetchall()
		msg += u'\n• '+str(j)+' ... '
		for i in cm: msg += i[0] +', '
		msg = msg[:-2]
	msg = u'Всего команд: '+str(len(comms))+u' | Префикс: '+get_prefix(get_local_prefix(jid))+u' | Ваш доступ: '+str(access_mode)+u' | Доступно команд: '+str(len(cu.execute('select * from tempo where am<=?',(access_mode,)).fetchall()))+msg
	tmp.close()
	send_msg(type, jid, nick, msg)
	
def helpme(type, jid, nick, text):
	if text == u'about': msg = u'Isida Jabber-bot | © 2oo9 Disabler Production Lab. | http://isida.googlecode.com'
	elif text == u'donation': msg = u'Реквизиты для благодарностей/помощи:\nMWallet id: 9034035371\nYandexMoney: 41001384336826\nС Уважением, Disabler'
	elif text == u'доступ': msg = u'У бота 3 уровня доступа:\n0 - команды доступны всем без ограничений.\n1 - доступ не ниже администратора конференции.\n2 - команды управления и настроек бота. доступны только владельцу бота.'
	elif text != '':
		msg = u'Префикс команд: '+get_prefix(get_local_prefix(jid))+u', Доступна справка по командам:\n'
		tmpbase = sqlite3.connect(':memory:')
		cu = tmpbase.cursor()
		cu.execute('''create table tempo (level integer, name text, body text)''')
		for tmp in comms: cu.execute('insert into tempo values (?,?,?)', (tmp[0], tmp[1], tmp[4]))
		cm = cu.execute('select body from tempo where name=?',(text,)).fetchone()
		if cm: msg = cm[0]
		else:
			cm = cu.execute('select * from tempo order by name').fetchall()
			tmpbase.close()
       			for i in range(0,3):
				msg += '['+str(i)+'] '
				for tmp in cm:
					if tmp[0] == i and tmp[2] != u'': msg += tmp[1] + ', '
				msg = msg[:-2]+'\n'
	else: msg = u'Isida Jabber Bot - Информационно-справочный бот | http://isida.googlecode.com | © 2oo9 Disabler Production Lab. | Справка по командам: help команда'
	send_msg(type, jid, nick, msg)

def bot_rejoin(type, jid, nick, text):
	global lastserver, lastnick, confbase
	text=unicode(text)
	if len(text): text=unicode(text)
	else: text=jid
	if not text.count('@'): text+='@'+lastserver
	if not text.count('/'): text+='/'+lastnick
	lastserver = getServer(text)
	lastnick = getResourse(text)
	lroom = text
	if arr_semi_find(confbase, getRoom(lroom)) >= 0:
		pprint(u'rejoin '+text+' by '+nick)
		sm = u'Перезахожу по команде от '+nick
		leaveconf(text, domain, sm)
		zz = joinconf(text, domain)
		if zz != None: send_msg(type, jid, nick, u'Ошибка! '+zz)
	else:
		send_msg(type, jid, nick, u'хватит бухать! Меня нету в '+getRoom(lroom))
		pprint(u'never be in '+text)

def bot_join(type, jid, nick, text):
	global lastserver, lastnick, confs, confbase
	text=unicode(text)
	if text=='' or text.count(' '): send_msg(type, jid, nick, u'косяк с аргументами!')
	else:
		if not text.count('@'): text+='@'+lastserver
		if not text.count('/'): text+='/'+lastnick
		lastserver = getServer(text)
		lastnick = getResourse(text)
		lroom = text.index('/')
		lroom = text[:lroom]
		if arr_semi_find(confbase, lroom) == -1:				
			zz = joinconf(text, domain)
			if zz != None:
				send_msg(type, jid, nick, u'Ошибка! '+zz)
				pprint(u'*** Error join to '+text+' '+zz)
			else:
				confbase.append(text)
				writefile(confs,str(confbase))
				send_msg(type, jid, nick, u'зашла в '+text)
				pprint(u'join to '+text)

		elif confbase.count(text):
			send_msg(type, jid, nick, u'хватит бухать! Я уже в '+lroom+u' с ником '+lastnick)
			pprint(u'already in '+text)
		else:
			zz = joinconf(text, domain)
			if zz != None:
				send_msg(type, jid, nick, u'Ошибка! '+zz)
				pprint(u'*** Error join to '+text+' '+zz)
			else:
				confbase = arr_del_semi_find(confbase, lroom)
				confbase.append(text)
				send_msg(type, jid, nick, u'смена ника в '+lroom+u' на '+lastnick)
				writefile(confs,str(confbase))
				pprint(u'change nick '+text)

def bot_leave(type, jid, nick, text):
	global confs, confbase, lastserver, lastnick
	if len(confbase) == 1: send_msg(type, jid, nick, u'не могу выйти из последней конфы!')
	else:
		if text == '': text = jid
		if not text.count('@'): text+='@'+lastserver
		if not text.count('/'): text+='/'+lastnick
		lastserver = getServer(text)
		lastnick = getResourse(text)
		if len(text): text=unicode(text)
		else: text=jid
		lroom = text
		if ownerbase.count(getRoom(jid)): nick = getName(jid)
		if arr_semi_find(confbase, getRoom(lroom)) >= 0:
			confbase = arr_del_semi_find(confbase,getRoom(lroom))
			writefile(confs,str(confbase))
			send_msg(type, jid, nick, u'свалила из '+text)
			sm = u'Меня выводит '+nick
			leaveconf(getRoom(text), domain, sm)
			pprint(u'leave '+text+' by '+nick)
		else:
			send_msg(type, jid, nick, u'хватит бухать! Меня нету в '+lroom)
			pprint(u'never be in '+text)

def conf_pass(type, jid, nick, text):
	global psw
	text=unicode(text)
	if text!='': psw = text
	send_msg(type, jid, nick, u'Временный пароль \''+psw+'\'')

def conf_limit(type, jid, nick, text):
	global msg_limit
	text=unicode(text)
	if text!='':
		try: msg_limit = int(text)
		except: msg_limit = 1000
	send_msg(type, jid, nick, u'Временный лимит размера сообщений '+str(msg_limit))

def bot_plugin(type, jid, nick, text):
	global plname, plugins, execute, gtimer, gpresence, gmassage
	text = text.split(' ')
	do = ''
	nnick = ''
	if len(text)>0: do = text[0]
	if len(text)>1: nnick = text[1]+'.py'
	pprint('plugin '+do+' '+nnick)
	msg = ''
	if do == 'add':
		if not plugins.count(nnick) and os.path.isfile('plugins/'+nnick):
			plugins.append(nnick)
			presence_control = []
			message_control = []
			iq_control = []
			timer = []
			execfile('plugins/'+nnick)
			msg = u'Загружен плагин: '+nnick[:-3]+u'\nДоступны комманды: '
			for cm in execute:
				msg += cm[1]+'['+str(cm[0])+'], '
				comms.append((cm[0],cm[1],cm[2],cm[3],u'Плагин '+nnick[:-3]+'. '+cm[4]))
			msg = msg[:-2]
			for tmr in timer: gtimer.append(tmr)
			for tmp in presence_control: gpresence.append(tmp)
			for tmp in message_control: gmessage.append(tmp)
	elif do == 'del':
		if plugins.count(nnick) and os.path.isfile('plugins/'+nnick):
			plugins.remove(nnick)
			presence_control = []
			message_control = []
			iq_control = []
			timer = []
			execfile('plugins/'+nnick)
			msg = u'Удалён плагин: '+nnick[:-3]+u'\nУдалены комманды: '
			for commmm in execute:
				msg += commmm[1]+'['+str(commmm[0])+'], '
				for i in comms:
					if i[1] == commmm[1]: comms.remove(i)
			msg = msg[:-2]
			for tmr in timer: gtimer.remove(tmr)
			for tmp in presence_control: gpresence.remove(tmp)
			for tmp in message_control: gmessage.remove(tmp)
	elif do == 'local':
		a = os.listdir('plugins/')
		b = []
		for c in a:
			if c[-3:] == u'.py' and c != 'main.py': b.append(c[:-3].decode('utf-8'))
		msg = u'Доступные плагины: '
		for c in b: msg += c+', '
		msg = msg[:-2]
	elif do == 'show':
		msg = u'Активные плагины: '
		for jjid in plugins: msg += jjid[:-3]+', '
		msg = msg[:-2]
	else: msg = u'Косяк с параметрами!'
	writefile(plname,str(plugins))
	send_msg(type, jid, nick, msg)

def owner(type, jid, nick, text):
	global ownerbase, owners, god
	do = text[:3]
	nnick = text[4:]
	pprint('owner '+do+' '+nnick)
	if do == 'add':
		if not ownerbase.count(nnick):
			ownerbase.append(nnick)
			j = Presence(nnick, 'subscribe')
			j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
			cl.send(j)
	elif do == 'del':
		if ownerbase.count(nnick) and nnick != god:
			ownerbase.remove(nnick)
			j = Presence(nnick, 'unsubscribed')
			j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
			cl.send(j)
	msg = u'Я принимаю команды от: '
	for jjid in ownerbase: msg += jjid+', '
	msg = msg[:-2]
	writefile(owners,str(ownerbase))
	send_msg(type, jid, nick, msg)

def ignore(type, jid, nick, text):
	global ignorebase, ignores, god
	do = text[:3]
	nnick = text[4:].lower()
	pprint('ignore '+do+' '+nnick)
	if do == 'add':
		if not ignorebase.count(nnick): ignorebase.append(nnick)
	elif do == 'del':
		if ignorebase.count(nnick) and nnick != god: ignorebase.remove(nnick)
	msg = u'Я не принимаю команды от: '
	for jjid in ignorebase:
		if jjid.count('@') and jjid.count('.'): msg += jjid+', '
		else: msg += '*'+jjid+'*, '
	msg = msg[:-2]
	writefile(ignores,str(ignorebase))
	send_msg(type, jid, nick, msg)

def info_where(type, jid, nick):
	global confbase
	msg = u'Активных конференций: '+str(len(confbase))+'\n'
	wbase = []
	for jjid in confbase:
		cnt = 0
		rjid = getRoom(jjid)
		for mega in megabase:
			if mega[0] == rjid: cnt += 1
		wbase.append((jjid, cnt))
	for i in range(0,len(wbase)-1):
		for j in range(i,len(wbase)):
			if wbase[i][1] < wbase[j][1]:
				jj = wbase[i]
				wbase[i] = wbase[j]
				wbase[j] = jj
	nmb = 1
	for i in wbase:
		msg += str(nmb)+'. '+i[0]+' ['+str(i[1])+']\n'
		nmb += 1
	msg = msg[:-1]
	send_msg(type, jid, nick, msg)

def get_uptime_raw():
	nowtime = tuple(localtime())
	difftime = [0,0,0,0,0,0]
	difftime[5] = nowtime[5]-starttime[5]
	if difftime[5] < 0:
		difftime[5] += 60
		difftime[4] -= 1
	difftime[4] += nowtime[4]-starttime[4]
	if difftime[4] < 0:
		difftime[4] += 60
		difftime[3] -= 1
	difftime[3] += nowtime[3]-starttime[3]
	if difftime[3] < 0:
		difftime[3] += 24
		difftime[2] -= 1
	timemonth = [31,28,31,30,31,30,31,31,30,31,30,31]
	difftime[2] += nowtime[2]-starttime[2]
	if difftime[2] < 0:
		difftime[2] += timemonth(nowtime[2])
		difftime[1] -= 1
	difftime[1] += nowtime[1]-starttime[1]
	if difftime[1] < 0:
		difftime[1] += 12
		difftime[0] -= 1
	difftime[0] += nowtime[0]-starttime[0]
	return difftime

def get_uptime_str():
	difftime = get_uptime_raw()
	msg = u''
	if difftime[0] >0: msg += str(difftime[0])+'y '
	if difftime[1] >0: msg += str(difftime[1])+'m '
	if difftime[2] >0: msg += str(difftime[2])+'d '
	msg += tZ(difftime[3])+':'+tZ(difftime[4])+':'+tZ(difftime[5])
	return msg

def info(type, jid, nick):
	global confbase	
	msg = u'Конференций: '+str(len(confbase))+u' (подробнее where)\n'
	msg += u'Сервер: '+lastserver+u' | Ник: '+lastnick+'\n'
	msg += u'Лимит размера сообщений: '+str(msg_limit)+'\n'
	msg += u'Время запуска: '+timeadd(starttime)+'\n'
	msg += u'Локальное время: '+timeadd(tuple(localtime()))+'\n'
	msg += u'Время работы: ' + get_uptime_str()+u', Последняя сессия: '+un_unix(int(time.time())-sesstime)
	smiles = getFile(sml,[(getRoom(jid),0)])
	msg += u'\nSmiles: ' + onoff(int((getRoom(jid),1) in smiles))
	floods = getFile(fld,[(getRoom(jid),0)])
	msg += u' | Flood: ' + onoff(int((getRoom(jid),1) in floods))
	gl_censor = getFile(cns,[(getRoom(jid),0)])
	msg += u' | Censor: ' + onoff(int((getRoom(jid),1) in gl_censor))
	msg += u' | Префикс команд: '+get_prefix(get_local_prefix(jid))
	send_msg(type, jid, nick, msg)

def info_res(type, jid, nick, text):
	mdb = sqlite3.connect(jid_base)
	cu = mdb.cursor()
	if text == 'count':
		tlen = len(cu.execute('select resourse,count(*) from jid group by resourse order by -count(*)').fetchall())
		jidbase = []
	elif text == '':
		tlen = len(cu.execute('select resourse,count(*) from jid group by resourse order by -count(*)').fetchall())
		jidbase = cu.execute('select resourse,count(*) from jid group by resourse order by -count(*)').fetchmany(10)
	else:
		text1 = '%'+text+'%'
		tlen = len(cu.execute('select resourse,count(*) from jid where resourse like ? group by resourse order by -count(*)',(text1,)).fetchall())
		jidbase = cu.execute('select resourse,count(*) from jid where resourse like ? group by resourse order by -count(*)',(text1,)).fetchmany(10)
	if not tlen: msg = u'Не найдено: '+text
	else:
		if text == '': msg = u'Всего ресурсов: '+str(tlen)+' \n'
		else: msg = u'Найдено ресурсов: '+str(tlen)+' \n'
		cnt = 1
		for jj in jidbase:
			msg += str(cnt)+'. '+jj[0]+'\t'+str(jj[1])+' \n'
			cnt += 1
		msg = msg[:-2]
	send_msg(type, jid, nick, msg)

def info_serv(type, jid, nick, text):
	mdb = sqlite3.connect(jid_base)
	cu = mdb.cursor()
	if text == 'count':
		tlen = len(cu.execute('select server,count(*) from jid group by server order by -count(*)').fetchall())
		jidbase = []
	elif text == '':
		tlen = len(cu.execute('select server,count(*) from jid group by server order by -count(*)').fetchall())
		jidbase = cu.execute('select server,count(*) from jid group by server order by -count(*)').fetchall()
	else:
		text1 = '%'+text+'%'
		tlen = len(cu.execute('select server,count(*) from jid where server like ? group by server order by -count(*)',(text1,)).fetchall())
		jidbase = cu.execute('select server,count(*) from jid where server like ? group by server order by -count(*)',(text1,)).fetchall()
	if not tlen: msg = u'Не найдено: '+text
	else:
		if text == '': msg = u'Всего серверов: '+str(tlen)+' \n'
		else: msg = u'Найдено серверов: '+str(tlen)+' \n'
		for jj in jidbase: msg += jj[0]+':'+str(jj[1])+' | '
		msg = msg[:-2]
	send_msg(type, jid, nick, msg)

def info_base(type, jid, nick):
	msg = u'Чего искать то будем?'
	if nick != '':
		msg = u'Ты виден мне как '
		fl = 1
		for base in megabase:
			if base[1].count(nick):
				if base[0].lower() == jid:
# 0 - конфа
# 1 - ник
# 2 - роль
# 3 - аффиляция
# 4 - jid
#					msg += '\n'+base[0]+' '+base[1]+' '+base[2]+' '+base[3] +' '+base[4]
					msg += base[2]+'/'+base[3]
					fl = 0
		if fl: msg = '\''+nick+u'\' not found!'
	send_msg(type, jid, nick, msg)
	

def info_search(type, jid, nick, text):
	msg = u'Чего искать то будем?'
	if text != '':
		mdb = sqlite3.connect(jid_base)
		cu = mdb.cursor()
		ttext = '%'+text+'%'
		tma = cu.execute('select * from jid where login like ? or server like ? or resourse like ? order by login',(ttext,ttext,ttext)).fetchmany(10)
		if len(tma):
			msg = u'Найдено:'
			cnd = 1
			for tt in tma:
				msg += u'\n'+str(cnd)+'. '+tt[0]+'@'+tt[1]+'/'+tt[2]
				cnd += 1
		else: msg = text +u' не найдено!'
	send_msg(type, jid, nick, msg)

def gtmp_search(type, jid, nick, text):
	msg = u'Чего искать то будем?'
	if text != '':
		msg = u'Найдено:'
		fl = 1
		for mega1 in megabase2:
			for mega2 in mega1:
				if mega2.lower().count(text.lower()):
					msg += u'\n'+unicode(mega1[1])+u' is '+unicode(mega1[2])+u'/'+unicode(mega1[3])
					if mega1[4] != 'None':
						msg += u' ('+unicode(mega1[4])+u')'
					msg += ' in '+unicode(mega1[0])
					fl = 0
					break
		if fl: msg = '\''+text+u'\' not found!'
	send_msg(type, jid, nick, msg)

def tmp_search(type, jid, nick, text):
	msg = u'Чего искать то будем?'
	if text != '':
		msg = u'Найдено:'
		fl = 1
		for mega1 in megabase2:
			if getRoom(mega1[0]) == getRoom(jid):
				for mega2 in mega1:
					if mega2.lower().count(text.lower()):
						msg += u'\n'+unicode(mega1[1])+u' is '+unicode(mega1[2])+u'/'+unicode(mega1[3])
						if mega1[4] != 'None': msg += u' ('+unicode(mega1[4])+u')'
#						msg += ' in '+unicode(mega1[0])
						fl = 0
						break
		if fl: msg = '\''+text+u'\' not found!'
	send_msg(type, jid, nick, msg)


def real_search_owner(type, jid, nick, text):
	msg = u'Чего искать то будем?'
	if text != '':
		msg = u'Найдено:'
		fl = 1
		for mega1 in megabase:
			if mega1[2] != 'None' and mega1[3] != 'None':
				for mega2 in mega1:
					if mega2.lower().count(text.lower()):
						msg += u'\n'+unicode(mega1[1])+u' is '+unicode(mega1[2])+u'/'+unicode(mega1[3])
						if mega1[4] != 'None': msg += u' ('+unicode(mega1[4])+u')'
						msg += ' in '+unicode(mega1[0])
						fl = 0
						break
		if fl: msg = '\''+text+u'\' not found!'
	send_msg(type, jid, nick, msg)	

def real_search(type, jid, nick, text):
	msg = u'Чего искать то будем?'
	if text != '':
		msg = u'Найдено:'
		fl = 1
		for mega1 in megabase:
			if mega1[2] != 'None' and mega1[3] != 'None':
				for mega2 in mega1:
					if mega2.lower().count(text.lower()):
						msg += u'\n'+unicode(mega1[1])+u' is '+unicode(mega1[2])+u'/'+unicode(mega1[3])
						msg += ' in '+unicode(mega1[0])
						fl = 0
						break
		if fl: msg = '\''+text+u'\' not found!'
	send_msg(type, jid, nick, msg)

def isNumber(text):
	try:
		it = int(text,16)
		if it >= 32 and it <= 127: return chr(int(text,16))
		else: return '?'
	except: return 'None'

def rss_replace(ms):
	rmass = (('<br>','\n'),('<br />','\n'),('<br/>','\n'),('\n\r','\n'),('<![CDATA[',''),(']]>',''),('&lt;','<'),('&gt;','>'),('&quot;','\"'),('&apos;','\''),('&amp;','&'),('&middot;',u'·'),('&nbsp;',''),('&raquo;',u'▼'),('&copy;',u'©'))
	for tmp in rmass: ms = ms.replace(tmp[0],tmp[1])
	mm = ''
	m = 0
	while m<len(ms):
		try:
			if ms[m:m+2] == u'&#' and ms[m+6] == ';':
					mm += u'—'
					m += 6
			else: mm += ms[m]
		except: mm += ms[m]
		m += 1
# &#x2212;
	return mm

def rss_repl_html(ms):
	i=0
	lms = len(ms)
	while i < lms:
		if ms[i] == '<':
			for j in range(i, lms):
				if ms[j] == '>':
					break
			ms = ms[:i] +' '+ ms[j+1:]
			lms = len(ms)
			i -= 1
		i += 1
	return ms

def rss_del_html(ms):
	i=0
	lms = len(ms)
	while i < lms:
		if ms[i] == '<':
			for j in range(i, lms):
				if ms[j] == '>':
					break
			ms = ms[:i] + ms[j+1:]
			lms = len(ms)
			i -= 1
		i += 1
	return ms

def rss_del_nn(ms):
	while ms.count('  '):
		ms = ms.replace('  ',' ')
	ms = ms.replace('\r','')
	ms = ms.replace('\t','')
	ms = ms.replace('\n \n','\n')
	while ms.count('\n\n'):
		ms = ms.replace('\n\n','\n')
	ms += '\n'
	return ms

def html_encode(body):
	encidx = body.find('encoding=')
	if encidx >= 0:
		enc = body[encidx+10:encidx+30]
		enc = enc[:enc.find('?>')-1]
	else:
		encidx = body.find('charset=')
		if encidx >= 0:
			enc = body[encidx+8:encidx+30]
			enc = enc[:enc.find('"')]
		else: enc = chardet.detect(body)['encoding']

	if body == None: body = ''
	if enc == None or enc == '': enc = 'utf-8'
	return unicode(body,enc)

#[room, nick, role, affiliation, jid]

def rss(type, jid, nick, text):
	global feedbase, feeds,	lastfeeds, lafeeds
	msg = u'rss show|add|del|clear|new|get'
	nosend = 0
	text = text.split(' ')
	tl = len(text)

	if tl < 5: text.append('!')
		
	mode = text[0].lower() # show | add | del | clear | new | get

	if mode == 'add':
		if tl < 4:
			msg = 'rss add [http://]url timeH|M [full|body|head]'
			mode = ''
	elif mode == 'del':
		if tl < 2:
			msg = 'rss del [http://]url'
			mode = ''
	elif mode == 'new':
		if tl < 4:
			msg = 'rss new [http://]url max_feed_humber [full|body|head]'
			mode = ''
	elif mode == 'get':
		if tl < 4:
			msg = 'rss get [http://]url max_feed_humber [full|body|head]'
			mode = ''

	feedbase = getFile(feeds,[])
	lastfeeds = getFile(lafeeds,[])

	if mode == 'clear':
		msg = u'All RSS was cleared!'
		tf = []
		for taa in feedbase:
			if taa[4] != jid: tf.append(taa)
		feedbase = tf
		writefile(feeds,str(feedbase))

		tf = []
		for taa in lastfeeds:
			if taa[2] == jid: tf.append(taa)
		lastfeeds = tf
		writefile(lafeeds,str(lastfeeds))

	if mode == 'all':
		msg = u'No RSS found!'
		if feedbase != []:
			stt = 1
			msg = u'All schedule feeds:'
			for rs in feedbase:
				msg += u'\n'+getName(rs[4])+'\t'+rs[0]+u' ('+rs[1]+u') '+rs[2]
				lt = rs[3]
				msg += u' '+tZ(lt[2])+u'.'+tZ(lt[1])+u'.'+tZ(lt[0])+u' '+tZ(lt[3])+u':'+tZ(lt[4])+u':'+tZ(lt[5])
				stt = 0
			if stt: msg+= u' not found!'

	if mode == 'show':
		msg = u'No RSS found!'
		if feedbase != []:
			stt = 1
			msg = u'Schedule feeds for '+jid+u':'
			for rs in feedbase:
				if rs[4] == jid:
					msg += u'\n'+rs[0]+u' ('+rs[1]+u') '+rs[2]
					lt = rs[3]
					msg += u' '+tZ(lt[2])+u'.'+tZ(lt[1])+u'.'+tZ(lt[0])+u' '+tZ(lt[3])+u':'+tZ(lt[4])+u':'+tZ(lt[5])
					stt = 0
			if stt: msg+= u' not found!'

	elif mode == 'add':
			
		lt=tuple(localtime())
		link = text[1]
		if link[:7] != 'http://': link = 'http://'+link
		for dd in feedbase:
			if dd[0] == link and dd[4] == jid:
				feedbase.remove(dd)
				break
		feedbase.append([link, text[2], text[3], lt[:6], getRoom(jid)]) # url time mode
		writefile(feeds,str(feedbase))

		msg = u'Add feed to schedule: '+link+u' ('+text[2]+u') '+text[3]
		send_msg(type, jid, nick, msg)

		f = urllib.urlopen(link)
		feed = f.read()
		f.close()

		is_rss_aton = 0
		if feed[:256].count('rss') and feed[:256].count('xml'): is_rss_aton = 1
		elif feed[:256].count('http://www.w3.org/2005/Atom') and feed[:256].count('xml'): is_rss_aton = 2

		if is_rss_aton:
			feed = html_encode(feed)

			if feed.count('<items>'): feed = get_tag(feed,'items')

			if is_rss_aton == 1: feed = feed.split('<item')
			else: feed = feed.split('<entry>')

			if len(text) > 3: submode = text[3]
			else: submode = 'full'

			msg = 'Feeds for '
			if submode[-4:] == '-url':
				submode = submode[:-4]
				urlmode = 1

			else:
				urlmode = 0
				msg += link+' '

			msg += get_tag(feed[0],'title') + '\n'
			mmsg = feed[1]
			if is_rss_aton==1: mmsg = get_tag(mmsg,'title') + '\n'
			else: mmsg = ttitle = get_tag(mmsg,'content') + '\n'

			for dd in lastfeeds:
				if dd[0] == link and dd[2] == jid:
					lastfeeds.remove(dd)
					break
			lastfeeds.append([link,mmsg,jid])
			writefile(lafeeds,str(lastfeeds))

			mmsg = feed[1]
			if is_rss_aton==1:
				ttitle = get_tag(mmsg,'title')
				tbody = get_tag(mmsg,'description')
				turl = get_tag(mmsg,'link')
			else:
				ttitle = get_tag(mmsg,'content')
				tbody = get_tag(mmsg,'title')
				tu1 = mmsg.index('<link')
				tu2 = mmsg.find('href=\"',tu1)+6
				tu3 = mmsg.find('\"',tu2)
				turl = mmsg[tu2:tu3]

			msg += u' • '
			if submode == 'full':
				msg += ttitle+ '\n'
				msg += tbody + '\n\n'
			elif submode == 'body': msg += tbody + '\n'
			elif submode[:4] == 'head': msg += ttitle + '\n'
			if urlmode: msg += turl+'\n'

			msg = replacer(msg)

			msg = msg[:-1]
			if submode == 'full': msg = msg[:-1]
		else:
			feed = html_encode(feed)
			title = get_tag(feed,'title')
			msg = u'bad url or rss/atom not found at '+link+' - '+title

#---------

	elif mode == 'del':
		link = text[1]
		if link[:7] != 'http://': link = 'http://'+link

		bedel1 = 0
		for rs in feedbase:
			if rs[0] == link and rs[4] == jid:
				feedbase.remove(rs)
				bedel1 = 1

		bedel2 = 0
		for rs in lastfeeds:
			if rs[0] == link and rs[2] == jid:
				lastfeeds.remove(rs)
				bedel2 = 1

		if bedel1 or bedel2: msg = u'Delete feed from schedule: '+link
		if bedel1: writefile(feeds,str(feedbase))
		if bedel2: writefile(lafeeds,str(lastfeeds))
		else: msg = u'Can\'t find in schedule: '+link

	elif mode == 'new' or mode == 'get':
		link = text[1]
		if link[:7] != 'http://': link = 'http://'+link
		f = urllib.urlopen(link)
		feed = f.read()
		f.close()

		is_rss_aton = 0
		if feed[:256].count('rss') and feed[:256].count('xml'): is_rss_aton = 1
		elif feed[:256].count('http://www.w3.org/2005/Atom') and feed[:256].count('xml'): is_rss_aton = 2

		if is_rss_aton:
			feed = html_encode(feed)
			if feed.count('<items>'): feed = get_tag(feed,'<items>')

			if is_rss_aton == 1: feed = feed.split('<item')
			else: feed = feed.split('<entry>')
	
			if len(text) > 2: lng = int(text[2])+1
			else: lng = len(feed)
				
			if len(feed) <= lng: lng = len(feed)
			if lng>=11: lng = 11

			if len(text) > 3: submode = text[3]
			else: submode = 'full'

			msg = 'Feeds for '
			if submode[-4:] == '-url':
				submode = submode[:-4]
				urlmode = 1
			else:
				urlmode = 0
				msg += link+' '

			tstop = ''
			for ii in lastfeeds:
				if ii[2] == jid and ii[0] == link:
					 tstop = ii[1]
					 tstop = tstop[:-1]

			msg += get_tag(feed[0],'title') + '\n'
			mmsg = feed[1]
			if is_rss_aton==1: mmsg = get_tag(mmsg,'title') + '\n'
			else: mmsg = ttitle = get_tag(mmsg,'content') + '\n'

			for dd in lastfeeds:
				if dd[0] == link and dd[2] == jid:
					lastfeeds.remove(dd)
					break
			lastfeeds.append([link,mmsg,jid])
			writefile(lafeeds,str(lastfeeds))

			for mmsg in feed[1:lng]:
				if is_rss_aton == 1:
					ttitle = get_tag(mmsg,'title')
					tbody = get_tag(mmsg,'description')
					turl = get_tag(mmsg,'link')
				else:
					ttitle = get_tag(mmsg,'content')
					tbody = get_tag(mmsg,'title')
					tu1 = mmsg.index('<link')
					tu2 = mmsg.find('href=\"',tu1)+6
					tu3 = mmsg.find('\"',tu2)
					turl = mmsg[tu2:tu3]

				if mode == 'new':
					if ttitle == tstop: break
				msg += u' • '
				if submode == 'full':
					msg += ttitle + '\n'
					msg += tbody + '\n\n'
				elif submode == 'body': msg += tbody + '\n'
				elif submode[:4] == 'head': msg += ttitle+ '\n'
				if urlmode: msg += turl+'\n'

			if mode == 'new':
				if mmsg == feed[1] and text[4] == 'silent': nosend = 1
				elif mmsg == feed[1] and text[4] != 'silent': msg = 'New feeds not found! '

			if submode == 'body' or submode == 'head': msg = msg[:-1]

			msg = replacer(msg)
			msg = msg[:-1]

			if lng > 1 and submode == 'full': msg = msg[:-1]
		else:
			if text[4] == 'silent': nosend = 1
			else:
				feed = html_encode(feed)
				title = get_tag(feed,'title')
				msg = u'bad url or rss/atom not found at '+link+' - '+title
	if not nosend: send_msg(type, jid, nick, msg)

#------------------------------------------------

# в начале
# 0 - всем
# 1 - админам\овнерам
# 2 - владельцу бота

# в конце
# 1 - ничего не передавать
# 2 - передавать остаток текста

comms = [
	 (0, u'help', helpme, 2, u'Показывает текущие разделы справочной системы.'),
	 (2, u'join', bot_join, 2, u'Вход в конференцию:\njoin room@conference.server.ru/nick - вход в конференцию room с ником nick.\njoin room@conference.server.ru - вход в конференцию room с последним заданным ником.\njoin room - вход в конференцию room на последнем заданном сервере с последним заданным ником.'),
	 (2, u'leave', bot_leave, 2, u'Выход из конференции:\nleave - выход из текущей конференции.\nleave room - выход из конференции room на последнем заданном сервере.\nleave room@conference.server.ru - выход из конференции room'),
	 (2, u'rejoin', bot_rejoin, 2, u'Перезаход в конференцию.\nrejoin - перезайти в текущую конференцию.\nrejoin room - перезайти в конференцию room на последнем заданном сервере.\nrejoin room@conference.server.ru - перезайти в конференцию room'),
	 (2, u'pass', conf_pass, 2, u'Временный пароль для входа в конференции.'),
	 (2, u'bot_owner', owner, 2, u'Работа со списком владельцев бота:\nbot_owner show - показать список владельцев.\nbot_owner add jid - добавить jid в список.\nbot_owner del jid - удалить jid из списка.'),
	 (2, u'bot_ignore', ignore, 2, u'Работа с "Чёрным списком":\nbot_ignore show - показать список.\nbot_ignore add jid - добавить jid в список.\nbot_ignore del jid - удалить jid из списка.'),
	 (1, u'where', info_where, 1, u'Показ конференций, в которых находится бот. Так же показывается ник бота в конференции и количество участников.'),
	 (1, u'res', info_res, 2, u'Без параметра показывает топ10 рессурсов по всем конференциям, где находится бот.\nС параметром - поиск по базе рессурсов.\nЧисла - количество рессурсов.'),
	 (1, u'serv', info_serv, 2, u'Без параметра показывает все сервера, с которых заходили в конференции, где находится бот.\nС параметром - поиск по базе серверов.\nЕсли параметр count - показывает количество уникальных серверов.\nЧисла - количество серверов.'),
	 (0, u'inbase', info_base, 1, u'Идентификация Вас в глобальной базе.'),
	 (2, u'search', info_search, 2, u'Поиск по внутренней базе jid\'ов.'),
	 (1, u'look', real_search, 2, u'Поиск участника по конференциям, где находится бот.'),
	 (2, u'glook', real_search_owner, 2, u'Поиск участника по конференциям, где находится бот. Дополнительно будут показаны jid\'ы, если они видны боту.'),
	 (1, u'tempo', tmp_search, 2, u'Локальный поиск во временной базе.'),
	 (2, u'gtempo', gtmp_search, 2, u'Глобальный поиск во временной базе.'),
	 (1, u'rss', rss, 2, u'Каналы новостей:\nrss show - показать текущие подписки.\nrss add url time mode - добавить подписку.\nrss del url - удалить подписку.\nrss get url feeds mode - получить текущие новости.\nrss new url feeds mode - получить только не прочтенные новости.\nrss clear - удалить все новости в текущей конференции.\nrss all - показать все новости во всех конференциях.\n\nurl - адрес rss канала. можно задавать без http://\ntime - время обновления канала. число + указатель времени. H - часы, M - минуты. допускается только один указатель.\nfeeds - количество сообщений для получения. не более 10 шт.\nmode - режим получения сообщений. full - сообщения полностью, head - только заголовки, body - только тело сообщения.\nокончанием -url будет ещё показана url новости.'),
	 (1, u'alias', alias, 2, u'Сокращённые команды.\nalias add aa=bb - выполнить команду bb при написании команды aa\nalias del aa - удалить сокращение aa\nalias show [text] - показать все сокращения или похожие на text.'),
	 (0, u'commands', info_comm, 1, u'Показывает список доступных комманд.'),
	 (1, u'comm', comm_on_off, 2, u'Включение/выключение команд.\ncomm - показать список\ncomm on команда - включить команду\ncomm off команда1[ команда2 команда3 ...] - отключить одну или несколько команд'),
	 (0, u'bot_uptime', uptime, 1, u'Время работы бота.'),
	 (1, u'info', info, 1, u'Различная информация о боте.'),
	 (0, u'new', svn_info, 1, u'Показ svn-лога последнего обновления бота'),
	 (1, u'smile', smile, 2, u'Реакция смайлами на смену роли/аффиляции в данной конференции.\nsmile [on|off]'),
	 (1, u'flood', autoflood, 2, u'Включение/выключение самообучающегося автоответчика.\nflood [on|off]'),
	 (1, u'censor', censor_status, 2, u'Включение/выключение цензор-нотификатора.\ncensor [on|off]'),
	 (2, u'limit', conf_limit, 2, u'Размер сообщения, свыше которого сообщения будут разбиавться на части кратные этому размеру.'),
	 (2, u'plugin', bot_plugin, 2, u'Управление системой плагинов:\nplugin show - показать подключенные плагины.\nplugin local - показать доступные для подключения плагины.\nplugin add name.py - добавить плагин.\nplugin del name.py - удалить плагин.'),
	 (2, u'error', show_error, 2, u'Показывает последнюю логированную ошибку или последние, если задан параметр.\nerror [number|clear]'),
	 (0, u'whoami', info_access, 1, u'Ваша идентификация перед ботом.'),
	 (0, u'whois', info_whois, 2, u'Идентификация перед ботом.'),
	 (0, u'status', status, 2, u'Показ статуса.'),
	 (1, u'prefix', set_prefix, 2, u'Указание префикса комманд. Без параметра показывает текущий префикс. Если параметром будет none - префикс будет отключен.')]
