# -*- coding: utf-8 -*-

def true_age(type, jid, nick, text):
	text = text.split(' ')
	llim = 10
	if len(text)>=2:
		try:
			llim = int(text[0])
		except:
			llim = 10

		text = text[1]
	else:
		text = text[0]

	if llim > 100:
		llim = 100
	if text == '':
		text = nick
	is_found = 0
	ms = []
	for aa in agebase:
		if aa[0]==jid and (aa[1].lower().count(text.lower()) or aa[2].lower().count(text.lower())):
			if aa[5]:
				r_age = aa[4]
			else:
				r_age = int(time.time())-aa[3]+aa[4]
			ms.append((aa[1],r_age))
			is_found = 1
	if is_found:
		lms = len(ms)
		for i in range(0,lms-1):
			for j in range(i,lms):
				if ms[i][1] < ms[j][1]:
					jj = ms[i]
					ms[i] = ms[j]
					ms[j] = jj
		if lms > llim:
			lms = llim
		msg = u'Возраст:'
		for i in range(0,lms):
			msg += '\n'+ms[i][0]+'\t'+str(ms[i][1])
	else:
		msg = u'Не найдено!'

#agebase.append((room, nick,getRoom(jid),tt,ab[4],0))
        send_msg(type, jid, nick, msg)

def close_age():
	global agest, agebase
	taa = []
	tt = int(time.time())
	for ab in agebase:
		taa.append((ab[0],ab[1],ab[2],tt,ab[4]+(tt-ab[3]),1))
	agebase = taa
	writefile(agest,unicode(agebase))

def weather_city(type, jid, nick, text):
	text = text.upper()
	text = text.split(' ')

	link = 'http://weather.noaa.gov/weather/'+text[0]+'_cc.html'
	f = urllib.urlopen(link)
	wzz = f.read()
	f.close()

	if wzz.count('Not Found'):
		msg = u'Я не знаю такой страны!'
	else:
		wzpos = wzz.find('<select name=\"cccc\">')
		wzz = wzz[wzpos:wzz.find('</select>',wzpos)]

		wzz = wzz.split('<OPTION VALUE=\"')
		msg = u'Города по запросу: '
		not_add = 1
		for wzzz in wzz:
			if wzzz.lower().count(text[1].lower()):
				msg += '\n'+wzzz.replace('\">',' -')[:-1]
				not_add = 0
		if not_add:
			msg = u'Такой город не найден!'

        send_msg(type, jid, nick, msg)

def defcode(type, jid, nick, text):
	dcnt = text[0]
	ddef = text[1:4]
	dnumber = text[4:]
	if text[:2] != '79':
		msg = u'Поиск только по мобильным телефонам России!'
	else:
		link = 'http://www.mtt.ru/info/def/index.wbp?def='+ddef+'&number='+dnumber+'&region=&standard=&date=&operator='
		f = urllib.urlopen(link)
		msg = f.read()
		f.close()

		encidx = msg.find('charset=')
		if encidx >= 0:
			enc = msg[encidx+8:encidx+30]
			enc = enc[:enc.index('\">')]
			enc = enc.upper()
		else:
			enc = 'UTF-8'

		msg = unicode(msg, enc)

		mbeg = msg.find('<INPUT TYPE=\"submit\" CLASS=\"submit\"')
		msg = msg[mbeg:msg.find('</table>',mbeg)]
		msg = msg.split('<tr')
		
		if msg[0].count(u'не найдено'):
			msg = u'Не найдено!'
		else:
			msg.remove(msg[0])
			mmsg = u'Найдено:\n'
			for mm in msg:
				tmm = mm
				tmm = rss_replace(tmm)
				tmm = rss_del_html(tmm)
				tmm = rss_replace(tmm)
				tmm = rss_del_nn(tmm)
				tmm = tmm[tmm.find('>')+1:]
				tmm = tmm.replace('\n','\t')
				mmsg += tmm[1:-2] + '\n'
			msg = mmsg[:-1]
	
       	send_msg(type, jid, nick, msg)
	
def weather_raw(type, jid, nick, text):
	text = text.upper()
	link = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/'+text+'.TXT'
	f = urllib.urlopen(link)
	msg = f.read()
	f.close()

	msg = msg[:-1]

	if msg.count('Not Found'):
		msg = u'Город не найден!'

        send_msg(type, jid, nick, msg)

def weather(type, jid, nick, text):
	text = text.upper()
	link = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/'+text+'.TXT'
	f = urllib.urlopen(link)
	wzz = f.read()
	f.close()

	if wzz.count('Not Found'):
		msg = u'Город не найден!'
	else:
		wzz = wzz.split('\n')
		msg = wzz[0][:wzz[0].find(')')+1]
		msg += '\n'+ wzz[1]

		if wzz[5][:6] == 'Weathe':
			wzzclo = wzz[5]
			wzz.remove(wzz[5])
		else:
			wzzclo = ''

		if wzz[4][:3] == 'Sky':
			wzzsky = wzz[4]
			wzz.remove(wzz[4])
		else:
			wzzsky = ''

		wzz1 = wzz[4].find(':')+1
		wzz2 = wzz[4].find('(',wzz1)
		wzz3 = wzz[4].find(')',wzz2)
		msg += '\n'+ wzz[4][:wzz1] + ' ' + wzz[4][wzz2+1:wzz3]

#		wzz1 = wzz[5].find(':')+1
#		wzz2 = wzz[5].find('(',wzz1)
#		wzz3 = wzz[5].find(')',wzz2)
#		msg += ', '+ wzz[5][:wzz1] + ' ' + wzz[5][wzz2+1:wzz3]

		wzz1 = wzz[2].find('(')
		wzz2 = wzz[2].find(')',wzz1)
		wzz3 = wzz[2].find(':',wzz2)
		msg += '\n'+ wzz[2][:wzz1-1] + wzz[2][wzz2+1:wzz3]

		msg += '\n'+ wzz[6]
		if len(wzzsky):
			msg += ','+ wzzsky[wzzsky.find(':')+1:]
		if len(wzzclo):
			msg += ','+ wzzclo[wzzclo.find(':')+1:]
		if not (len(wzzsky)+len(wzzclo)):
			msg += ', clear'

		msg += '\n'+ wzz[3][:-2]
		
		wzz1 = wzz[7].find('(')
		wzz2 = wzz[7].find(':',wzz1)
		wzz3 = wzz[7].find('(',wzz2)
		msg += ', '+ wzz[7][:wzz1-1]+': '+wzz[7][wzz3+1:-1]

        send_msg(type, jid, nick, msg)

def get_prefix():
	global prefix
	if prefix != u'':
	        return prefix
	else:
		return u'отсутствует'

def update_prefix(old,new,com):
        tcom = []
        for ccom in com:
                ttcom = ccom
                if ccom[1][:len(old)] == old:
                        ttcom = []
                        ttcom.append(ccom[0])
                        ttcom.append(new + ccom[1][len(old):])
                        for tapp in ccom[2:]:
                                ttcom.append(tapp)
                tcom.append(ttcom)
        return tcom

def set_prefix(type, jid, nick, text):
        global preffile, prefix, comms
        old_prefix = prefix
	msg = u'Префикс комманд: '
        if os.path.isfile(preffile):
		pref = eval(readfile(preffile))
		prefix = pref[0]
	else:
		pref = [(u'_')]
		writefile(preffile,pref)
		prefix = pref[0]

        if text != '':
                prefix = text

	if text.lower() == 'none':
		prefix = u''

	msg += get_prefix()

	pref = [(prefix)]
        writefile(preffile,str(pref))
	send_msg(type, jid, nick, msg)

        comms = update_prefix(old_prefix, prefix, comms)
	

def inban(type, jid, nick, text):
	global banbase
	banbase = []
	i = Node('iq', {'id': randint(1,1000), 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'outcast'})])])
	cl.send(i)
	while banbase == []:
		sleep(0.5)
	msg = u'Всего в бане: '+str(len(banbase))
	if text != '':
		mmsg = u', найдено:\n'
		fnd = 1
		for i in banbase:
			if i[0].lower().count(text.lower()) or i[1].lower().count(text.lower()):
				mmsg += i[0]+' - '+i[1]+'\n'
				fnd = 0
		mmsg = mmsg[:-1]
		if fnd:
			mmsg = u', совпадений нет!'
		msg += mmsg
	banbase = []
        send_msg(type, jid, nick, msg)

def youtube(type, jid, nick, text):
	text = text.lower()
	text = text.encode('utf-8')
	text = text.replace('\\x','%')
	text = text.replace(' ','%20')
	link = 'http://www.youtube.com/results?search_type=&search_query='+text+'&aq=f'
	f = urllib.urlopen(link)
	tube = f.read()
	f.close()
#	tube = tube.split('video-title video-title-results')
	tube = tube.split('video-run-time')

	tmass = []
	ltube = len(tube)
	smsg = u'Всего найдено: '+str(ltube-1)
	if ltube > 4:
		ltube=4
	for i in range(1,ltube):

		msg = tube[i].decode('utf')
		idx = msg.index('>')
		imsg = msg[idx+1:]
		idx = imsg.index('<')
		mtime = imsg[:idx]

		idx = msg.index('/watch?v=')
		imsg = msg[idx:]
		idx = imsg.index('\"')
		imsg = imsg[:idx]
		murl = 'http://www.youtube.com'+imsg

		idx = msg.index('title=\"')
		imsg = msg[idx+7:]
		idx = imsg.index('\"')
		imsg = imsg[:idx]
		imsg = rss_replace(imsg)
		msg = murl +'\t'+ imsg +' ('+ mtime +')'
		tmass.append(msg)
	
	msg = smsg + '\n'
	for i in tmass:
		msg += i + '\n'
	msg = msg[:-1]
        send_msg(type, jid, nick, msg)
	

def smile(type, jid, nick):
	sml = 'settings/smile'
	if os.path.isfile(sml):
		smiles = eval(readfile(sml))
	else:
		smiles = [(getRoom(jid),0)]
		writefile(sml,str(smiles))
	msg = u'Smiles is '
	is_found = 1
	for sm in smiles:
		if sm[0] == getRoom(jid):
			tsm = (sm[0],int(not sm[1]))
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
	msg = u'Время работы: '
	msg += get_uptime_str()

        send_msg(type, jid, nick, msg)
	

def null_vars():
        vars = {'none/visitor':0,
                'none/participant':0,
                'none/moderator':0,
                'member/visitor':0,
                'member/participant':0,
                'member/moderator':0,
                'admin/moderator':0,
                'owner/moderator':0}
	return vars

def gstats(type, jid, nick):
        msg = u'За время работы ('+get_uptime_str()+u') я видела всего:'
	vars = null_vars()

        for mega in megabase2:
                        ta = mega[3]+'/'+mega[2]
			for va in vars:
				if va == ta:
		                        vars[ta]+=1
        for va in vars:
                if vars[va]:
                        msg += '\n'+str(va)+' '+str(vars[va])

        send_msg(type, jid, nick, msg)
	

def stats(type, jid, nick):
        msg = u'За время работы ('+get_uptime_str()+u') я видела здесь:'
	vars = null_vars()

        for mega in megabase2:
                if mega[0] == jid:
                        ta = mega[3]+'/'+mega[2]
			for va in vars:
				if va == ta:
		                        vars[ta]+=1
        for va in vars:
                if vars[va]:
                        msg += '\n'+str(va)+' '+str(vars[va])

        send_msg(type, jid, nick, msg)
	

def show_error(type, jid, nick, text):
	if len(text)>0:
		cmd = int(text)
	else:
		cmd = 1

	if os.path.isfile(LOG_FILENAME):
		log = str(readfile(LOG_FILENAME))
                log = log.split('ERROR:')

                lll = len(log)
        	msg = u'Total Error(s): '+str(lll-1)+', Last:\n'
                for aa in range(lll-cmd,lll):
                        msg += log[aa]+'\n'
                msg = msg[:-2]
        else:
                msg = u'No Errors'
	send_msg(type, jid, nick, msg)
	

def get_log(type, jid, nick, text):
	text = text.split(' ')
	if len(text)>0:
		cmd = text[0]
	else:
		cmd = ''
	if len(text)>1:
		arg = text[1]
	else:
		arg = ''
	logt=localtime()

	if cmd == 'len':
		if arg == '':
			logfile = 'log/'+tZ(logt[0])+tZ(logt[1])+tZ(logt[2])
		else:
			logfile = 'log/'+arg
		if os.path.isfile(logfile):
			log = eval(readfile(logfile))
		else:
			log = []
			writefile(logfile,str(log))
		log_lm = len(str(log))/msg_limit
		msg = u'Log length for '+logfile+' is '+str(len(log))+' record(s) / '+str(log_lm)+' Messages with limit: '+str(msg_limit)
		send_msg(type, jid, nick, msg)
	
	if cmd == 'show':
		if arg == '':
			logfile = 'log/'+tZ(logt[0])+tZ(logt[1])+tZ(logt[2])
		else:
			logfile = 'log/'+arg
		if os.path.isfile(logfile):
			log = eval(readfile(logfile))
		else:
			log = []
			writefile(logfile,str(log))
		if len(text)>2:
			arg1 = text[2]
		else:
			arg1 = '0-'+str(len(log)-1)
		if arg == '':
			llog = len(log)
			if llog >= 5:
				lllim = 5
			else:
				lllim = llog
			arg1 = str(len(log)-lllim)+'-'+str(len(log))

#		print arg1

		arg1 = arg1.split('-')
		log_from = int(arg1[0])
		log_to = int(arg1[1])
		msg = u'Log:'
		for clog in range(log_from, log_to):
			msg += '\n'+log[clog]
		send_msg(type, jid, nick, msg)
	

def get_access(cjid, cnick):
	access_mode = 0
	jid = 'None'
	if cnick != nickname:
		for base in megabase:
			if base[1].count(cnick) and base[0].lower()==cjid:
				jid = base[4]
				if base[3]==u'admin' or base[3]==u'owner':
        				access_mode = 1

	if ownerbase.count(getRoom(jid)):
		access_mode = 2

	if ignorebase.count(getRoom(jid)):
		access_mode = -1

	if jid == 'None' and ownerbase.count(getRoom(cjid)):
		access_mode = 2

        return (access_mode, jid)

def info_access(type, jid, nick):
	global comms

        ta = get_access(jid,nick)

        access_mode = ta[0]
        realjid =ta[1]

	msg = u'Доступ: '+str(access_mode)
        tb = [u'Минимальный',u'Админ/Владелец конфы',u'Владелец бота']
        msg += ', ' + tb[access_mode]
	
        if realjid != 'None':
                msg += u', jid опознан'

	msg += u', Префикс: ' + get_prefix()
	send_msg(type, jid, nick, msg)
		

def info_comm(type, jid, nick):
	global comms
	msg = ''
	ccnt = 0
	jidc = comms

        ta = get_access(jid,nick)

        access_mode = ta[0]
        jid2 =ta[1]

        accs = [u'всем', u'админам/овнерам', u'владельцу бота']

        for i in range(0,3):
                msg += '['+str(i)+'] '+accs[i]+': '
        	for ccomms in jidc:
        		if not ccomms[1].count(god) and ccomms[0] == i:
                                ccc = ccomms[1]
                                if ccc[:len(prefix)] == prefix:
                                        ccc = ccc[len(prefix):]
        			msg += ccc +', '
#        			msg += ccomms[1] +', '
        			ccnt+= 1
                msg = msg[:-2] + '\n'
			
	msg = u'Команды парсера: '+str(ccnt)+u', Ваш доступ: '+str(access_mode)+u', Префикс: '+get_prefix()+'\n'+msg
	msg = msg[:-1]
	send_msg(type, jid, nick, msg)
	
        
def bot_exit(type, jid, nick, text):
	global game_over
	StatusMessage = u'Exit by \'quit\' command from bot owner ('+nick+u')'
	if text != '':
                StatusMessage += ' ['+text+u']'
	send_presence_all(StatusMessage)
	writefile('settings/tmp',str('exit'))
	sleep(3)
	game_over = 1
	sys.exit(0)	

def bot_restart(type, jid, nick, text):
	global game_over
	StatusMessage = u'Restart by \'restart\' command from bot owner ('+nick+u')'
	if text != '':
                StatusMessage += ' ['+text+u']'
	send_presence_all(StatusMessage)
	writefile('settings/tmp',str('restart'))
	game_over = 1
	sys.exit(0)	

def bot_update(type, jid, nick, text):
	global game_over
	StatusMessage = u'Self update by \'update\' command from bot owner ('+nick+u')'
	if text != '':
                StatusMessage += ' ['+text+u']'
	send_presence_all(StatusMessage)
	writefile('settings/tmp',str('update'))
	game_over = 1
	sys.exit(0)	

def say(type, jid, nick, text):
	nick = ''
	type = 'groupchat'
	send_msg(type, jid, nick, text)
	

def gsay(type, jid, nick, text):
        global confbase

	type = 'groupchat'
        msg = text
	nick = ''
        for jjid in confbase:
	        send_msg(type, getRoom(jjid), nick, msg)
	

def helpme(type, jid, nick, text):
	pprint(text)
	hlpfile = 'help/help.txt'
	helps = []
	if os.path.isfile(hlpfile):
		hlp = readfile(hlpfile)
		hlp = hlp.split('[')
		for hh in hlp:
			if len(hh):
				hh = hh.decode('utf-8')
				hhh = hh.split(']')
				helps.append((hhh[0],hhh[1][:-1]))

	mesg = u'Префикс команд: '+get_prefix()+u'\nДоступна справка по командам:\n'

        cnt = 0
        for i in range(0,3):
                mesg += '['+str(i)+'] '
        	for hlp in helps:
                        for cmdd in comms:
				tc = cmdd[1]
				if tc[:len(prefix)]==prefix:
					tc = tc[len(prefix):]
                                if tc == hlp[0] and cmdd[0] == i:
                                        mesg += hlp[0] + ', '
                                        cnt += 1
                mesg = mesg[:-2]
                mesg += '\n'
        if cnt != len(helps):
                mesg += '[?] '
                for hlp in helps:
                        fl = 1
                        for cmdd in comms:
				tc = cmdd[1]
				if tc[:len(prefix)]==prefix:
					tc = tc[len(prefix):]
                                if tc == hlp[0]:
                                        fl = 0
                        if fl:
                                mesg += hlp[0] + ', '
                mesg = mesg[:-1]
	mesg = mesg[:-1]

	for hlp in helps:
		if text.lower() == hlp[0]:
			mesg = u'Справочная информация: ' + hlp[1]
			for cmdd in comms:
				tc = cmdd[1]
				if tc[:len(prefix)]==prefix:
					tc = tc[len(prefix):]
                                if tc == hlp[0]:
                                        mesg = u'Уровень доступа: '+str(cmdd[0]) + hlp[1]

	send_msg(type, jid, nick, mesg)
	

def hidden_clear(type, jid, nick):
        pprint(u'clear: '+unicode(jid)+u' by: '+unicode(nick))
        cntr = 19                
        while (cntr>0):
                cl.send(xmpp.Message(jid, '', "groupchat"))
                time.sleep(1.05)
                cntr=cntr-1
        send_msg(type, jid, nick, u'стирильно!!!')
	

def bot_rejoin(type, jid, nick, text):
        global lastserver, lastnick, confbase
        text=unicode(text)

	if len(text):
		text=unicode(text)
	else:
		text=jid

	if toSymbolPosition(text,'@')<0:
		text+='@'+lastserver
	if toSymbolPosition(text,'/')<0:
		text+='/'+lastnick
                             
	lastserver = getServer(text)
	lastnick = getResourse(text)
	lroom = text
                                
	if arr_semi_find(confbase, getRoom(lroom)) >= 0:
		pprint(u'rejoin '+text+' by '+nick)
		sm = u'Перезахожу по команде от '+nick
		leaveconf(text, domain, sm)
		joinconf(text, domain)
	else:
		send_msg(type, jid, nick, u'хватит бухать! Меня нету в '+getRoom(lroom))
		pprint(u'never be in '+text)
	

def bot_join(type, jid, nick, text):
        global lastserver, lastnick, confs, confbase
        text=unicode(text)
        if text=='':
                send_msg(type, jid, nick, u'косяк с аргументами!')
        else:
                if toSymbolPosition(text,'@')<0:
                        text+='@'+lastserver
                if toSymbolPosition(text,'/')<0:
                        text+='/'+lastnick
                             
                lastserver = getServer(text)
                lastnick = getResourse(text)
                                
                lroom = text.index('/')
                lroom = text[:lroom]

		if arr_semi_find(confbase, lroom) == -1:                                
                        confbase.append(text)
                        joinconf(text, domain)
                        writefile(confs,str(confbase))
                        send_msg(type, jid, nick, u'зашла в '+text)
                        pprint(u'join to '+text)
                elif confbase.count(text):
                        send_msg(type, jid, nick, u'хватит бухать! Я уже в '+lroom+u' с ником '+lastnick)
                        pprint(u'already in '+text)
		else:
			confbase = arr_del_semi_find(confbase, lroom)
                        confbase.append(text)
			send_msg(type, jid, nick, u'смена ника в '+lroom+u' на '+lastnick)
                        joinconf(text, domain)
                        writefile(confs,str(confbase))
                        pprint(u'change nick '+text)
	

def bot_leave(type, jid, nick, text):
        global confs, confbase, lastserver, lastnick
        if len(confbase) == 1:
                send_msg(type, jid, nick, u'не могу выйти из последней конфы!')
        else:
		if text == '':
			text = getName(jid)
                if toSymbolPosition(text,'@')<0:
                        text+='@'+lastserver
                if toSymbolPosition(text,'/')<0:
                        text+='/'+lastnick
                             
                lastserver = getServer(text)
                lastnick = getResourse(text)

                if len(text):
                        text=unicode(text)
                else:
                        text=jid
                lroom = text
                              

		if ownerbase.count(getRoom(jid)):
			nick = getName(jid)
  
		if arr_semi_find(confbase, getRoom(lroom)) >= 0:
#                if confbase.count(lroom):
#                        confbase.remove(lroom)
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
	if text!='':
		psw = text
	send_msg(type, jid, nick, u'пароль \''+psw+'\'')
	

def conf_limit(type, jid, nick, text):
	global msg_limit
	text=unicode(text)
	if text!='':
		try:
			msg_limit = int(text)
		except:
			msg_limit = 1000
	send_msg(type, jid, nick, u'Message limit is '+str(msg_limit))
	

def bot_plugin(type, jid, nick, text):
	global plname, plugins, execute
	text = text.split(' ')
	do = ''
	nnick = ''
	if len(text)>0:
		do = text[0]
	if len(text)>1:
		nnick = text[1]
	pprint('plugin '+do+' '+nnick)
	msg = ''
	if do == 'add':
                if not plugins.count(nnick) and os.path.isfile('plugins/'+nnick):
                        plugins.append(nnick)
                        execfile('plugins/'+nnick)
                        msg = u'Загружен плагин: '+nnick+u'\nДоступны комманды: '
                        for commmm in execute:
                                msg += commmm[1]+'['+str(commmm[0])+'], '
                                comms.append(commmm)
                        msg = msg[:-2]
                        
	elif do == 'del':
                if plugins.count(nnick) and os.path.isfile('plugins/'+nnick):
                        plugins.remove(nnick)
                        execfile('plugins/'+nnick)
                        msg = u'Удалён плагин: '+nnick+u'\nУдалены комманды: '
                        for commmm in execute:
                                msg += commmm[1]+'['+str(commmm[0])+'], '
                                for i in comms:
                                        if i[1] == commmm[1]:
                                                comms.remove(i)
                        msg = msg[:-2]

	elif do == 'local':
		a = os.listdir('plugins/')
		b = []
		for c in a:
			if c[-3:] == u'.py' and c != 'main.py':
				b.append(c)
		msg = u'Доступные плагины: '
		for c in b:
				msg += c+', '
		msg = msg[:-2]
		
	else:
		msg = u'Активные плагины: '
		for jjid in plugins:
				msg += jjid+', '
		msg = msg[:-2]


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
	elif do == 'del':
                if ownerbase.count(nnick) and nnick != god:
                        ownerbase.remove(nnick)
#        elif do == 'clr':
#                ownerbase = [god]

	msg = u'Я принимаю команды от: '
	for jjid in ownerbase:
			msg += jjid+', '
	msg = msg[:-2]
	writefile(owners,str(ownerbase))
        send_msg(type, jid, nick, msg)
	

def ignore(type, jid, nick, text):
	global ignorebase, ignores, god
	do = text[:3]
	nnick = text[4:]
	pprint('ignore '+do+' '+nnick)
	if do == 'add':
                if not ignorebase.count(nnick):
                        ignorebase.append(nnick)
	elif do == 'del':
                if ignorebase.count(nnick) and nnick != god:
                        ignorebase.remove(nnick)
#        elif do == 'clr':
#                ignorebase = []

	msg = u'Я не принимаю команды от: '
	for jjid in ignorebase:
			msg += jjid+', '
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
			if mega[0] == rjid:
				cnt += 1
		wbase.append((jjid, cnt))

	for i in range(0,len(wbase)-1):
		for j in range(i,len(wbase)):
			if wbase[i][1] < wbase[j][1]:
				jj = wbase[i]
				wbase[i] = wbase[j]
				wbase[j] = jj
	for i in wbase:
		msg += i[0]+' ['+str(i[1])+']\n'

        msg = msg[:-1]
        send_msg(type, jid, nick, msg)
	

def get_uptime_raw():
	nowtime = localtime()

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
	if difftime[0] >0:
                msg += str(difftime[0])+'y '
	if difftime[1] >0:
                msg += str(difftime[1])+'m '
	if difftime[2] >0:
                msg += str(difftime[2])+'d '
        msg += tZ(difftime[3])+':'+tZ(difftime[4])+':'+tZ(difftime[5])
	return msg

def info(type, jid, nick):
        global confbase        
        msg = u'Конференций: '+str(len(confbase))+u' (подробнее where)\n'
        msg += u'Сервер: '+lastserver+'\n'
        msg += u'Ник: '+lastnick+'\n'
	msg += u'Лимит размера сообщений: '+str(msg_limit)+'\n'
	msg += u'Время запуска: '+timeadd(starttime)+'\n'
	nowtime = localtime()
	msg += u'Локальное время: '+timeadd(nowtime)+'\n'

	msg += u'Время работы: '
	msg += get_uptime_str()

        send_msg(type, jid, nick, msg)
	

def info_res(type, jid, nick, text):
	jidb = []
	jidc = []
	for jjid in jidbase:
		jserv = getResourse(jjid)
		if not jidb.count(jserv):
			jidb.append(jserv)
			jidc.append(1)
		else:
			jidc[jidb.index(jserv)] += 1
	msg = u'Уникальных рессурсов: '+str(len(jidb))+u' (Всего: '+str(len(jidbase))+')'
	if text == '':
		for i in range(0,len(jidc)-1):
			for j in range(i,len(jidc)):
				if jidc[i] < jidc[j]:
					jj = jidc[i]
					jidc[i] = jidc[j]
					jidc[j] = jj
					jj = jidb[i]
					jidb[i] = jidb[j]
					jidb[j] = jj
		if len(jidb)>9:
			jidbmax = 10
		else:
			jidbmax = len(jidb)
		for jji in range(0,jidbmax):# jidb:
                        jjid = jidb[jji]
			msg += '\n'+jjid+' '+str(jidc[jidb.index(jjid)])
	else:
                fl = 1
                for jjid in jidb:
                        if jjid.lower().count(text.lower()):
                        	msg += '\n'+jjid+' '+str(jidc[jidb.index(jjid)])
                        	fl = 0
                if fl:
                        msg += '\n'+text+u' Not found!'
        send_msg(type, jid, nick, msg)
	

def info_serv(type, jid, nick, text):
	jidb = []
	jidc = []
	for jjid in jidbase:
		jserv = getServer(jjid)
		if not jidb.count(jserv):
			jidb.append(jserv)
			jidc.append(1)
		else:
			jidc[jidb.index(jserv)] += 1
	msg = u'Уникальных серверов: '+str(len(jidb))+u' (Всего: '+str(len(jidbase))+')'
	if text == '':
		for i in range(0,len(jidc)-1):
			for j in range(i,len(jidc)):
				if jidc[i] < jidc[j]:
					jj = jidc[i]
					jidc[i] = jidc[j]
					jidc[j] = jj
					jj = jidb[i]
					jidb[i] = jidb[j]
					jidb[j] = jj

		for jjid in jidb:
			msg += ' | '+jjid+':'+str(jidc[jidb.index(jjid)])
	else:
                fl = 1
                for jjid in jidb:
                        if jjid.lower().count(text.lower()):
                        	msg += '\n'+jjid+' '+str(jidc[jidb.index(jjid)])
                        	fl = 0
                if fl:
                        msg += '\n'+text+u' Not found!'
        send_msg(type, jid, nick, msg)
	

def info_base(type, jid, nick):
        msg = u'Чего искать то будем?'
	if nick != '':
        	msg = u'Найдено:'
                fl = 1
                for base in megabase:
                        if base[1].lower().count(nick.lower()):
				if base[0].lower() == jid:
# 0 - конфа
# 1 - ник
# 2 - роль
# 3 - аффиляция
# 4 - jid
	                        	msg += '\n'+base[0]+' '+base[1]+' '+base[2]+' '+base[3] #+' '+base[4]
	                        	fl = 0
                if fl:
                        msg = '\''+nick+u'\' not found!'
        send_msg(type, jid, nick, msg)
	

def info_search(type, jid, nick, text):
        msg = u'Чего искать то будем?'
	if text != '':
        	msg = u'Найдено:'
                fl = 1
                for jjid in jidbase:
                        if jjid.lower().count(text.lower()):
                        	msg += '\n'+jjid
                        	fl = 0
                if fl:
                        msg = '\''+text+u'\' not found!'
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
                if fl:
                        msg = '\''+text+u'\' not found!'
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
						if mega1[4] != 'None':
							msg += u' ('+unicode(mega1[4])+u')'
						msg += ' in '+unicode(mega1[0])
        		                	fl = 0
						break
                if fl:
                        msg = '\''+text+u'\' not found!'
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
#						if mega1[4] != 'None':
#							msg += u' ('+unicode(mega1[4])+u')'
						msg += ' in '+unicode(mega1[0])
	        	                	fl = 0
						break
                if fl:
                        msg = '\''+text+u'\' not found!'
        send_msg(type, jid, nick, msg)
	

def rss_replace(ms):
	ms = ms.replace('<br>','\n')
	ms = ms.replace('<br />','\n')
	ms = ms.replace('<br/>','\n')
	ms = ms.replace('<![CDATA[','')
	ms = ms.replace(']]>','')
	ms = ms.replace('&lt;','<')
	ms = ms.replace('&gt;','>')
	ms = ms.replace('&quot;','\"')
	ms = ms.replace('&apos;','\'')
	ms = ms.replace('&amp;','&')
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
	ms = ms.replace('\n\n','\n')

	ms += '\n'

	return ms

#[room, nick, role, affiliation, jid]

feeds = 'settings/feed'
lafeeds = 'settings/lastfeeds'

def rss(type, jid, nick, text):
        msg = u'rss show|add|del|clear|new|get'
	nosend = 0
	text = text.lower()
        text = text.split(' ')
        tl = len(text)

        if tl < 5:
                text.append('!')
                
	mode = text[0] # show | add | del | clear | new | get

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

	if os.path.isfile(feeds):
		feedbase = eval(readfile(feeds))
	else:
		feedbase = []
		writefile(feeds,str(feedbase))

	if os.path.isfile(lafeeds):
		lastfeeds = eval(readfile(lafeeds))
	else:
		lastfeeds = []
		writefile(lafeeds,str(lastfeeds))

	if mode == 'clear':
		msg = u'All RSS was cleared!'
		tf = []
		for taa in feedbase:
			if taa[4] != jid:
				tf.append(taa)
		feedbase = tf
		writefile(feeds,str(feedbase))

		tf = []
		for taa in lastfeeds:
			if taa[2] == jid:
				tf.append(taa)
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
			if stt:
				msg+= u' not found!'

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
			if stt:
				msg+= u' not found!'

	elif mode == 'add':
                        
		lt=localtime()
		link = text[1]
		if link[:7] != 'http://':
        	        link = 'http://'+link
        	for dd in feedbase:
                        if dd[0] == link and dd[4] == jid:
                                feedbase.remove(dd)
		feedbase.append([link, text[2], text[3], lt[:6], jid]) # url time mode
		msg = u'Add feed to schedule: '+link+u' ('+text[2]+u') '+text[3]
		send_msg(type, jid, nick, msg)

		writefile(feeds,str(feedbase))
#---------
		f = urllib.urlopen(link)
		feed = f.read()
		f.close()

#		writefile('settings/tempofeed',str(feed))

		is_atom = feed[:100].count('http://www.w3.org/2005/Atom') and feed[:100].count('xml')
		is_rss = feed[:100].count('rss') and feed[:100].count('xml')

		if is_atom or is_rss:
			encidx = feed.find('encoding=')
			if encidx >= 0:
				enc = feed[encidx+10:encidx+30]
				enc = enc[:enc.index('?>')-1]
				enc = enc.upper()
			else:
				enc = 'UTF-8'

			feed = unicode(feed, enc)
			if is_rss:
		        	feed = feed.split('<item>')
			if is_atom:
		        	feed = feed.split('<entry>')
			msg = 'Feeds for '+link+' '

			lng = 2
			if len(feed) <= lng:
				lng = len(feed)
			if lng>=11:
				lng = 11

			if len(text) > 3:
				submode = text[3]
			else:
				submode = 'full'
			mmsg = feed[0]
			msg += mmsg[mmsg.index('<title>')+7:mmsg.index('</title>')]+ '\n'
			mmsg = feed[1]
			if is_rss:
				mmsg = mmsg[mmsg.index('<title>')+7:mmsg.index('</title>')]+ '\n'
			if is_atom:
				mmsg = mmsg[mmsg.find('>',mmsg.index('<content'))+1:mmsg.index('</content>')]+ '\n'
			for dd in lastfeeds:
                                if dd[0] == link and dd[2] == jid:
                                        lastfeeds.remove(dd)
			lastfeeds.append([link,mmsg,jid])
			writefile(lafeeds,str(lastfeeds))
			for idx in range(1,lng):
				mmsg = feed[idx]
				if is_rss:
					ttitle = mmsg[mmsg.index('<title>')+7:mmsg.index('</title>')]
					tbody = mmsg[mmsg.index('<description>')+13:mmsg.index('</description>')]
				if is_atom:
					ttitle = mmsg[mmsg.find('>',mmsg.index('<content'))+1:mmsg.index('</content>')]
					tbody = mmsg[mmsg.find('>',mmsg.index('<title'))+1:mmsg.index('</title>')]

				if submode == 'full':
					msg += u' • ' + ttitle+ '\n'
					msg += tbody + '\n\n'
				elif submode == 'body':
					msg += tbody + '\n'
				elif submode[:4] == 'head':
					msg += u' • ' + ttitle + '\n'
			msg = rss_replace(msg)
			msg = rss_del_html(msg)
			msg = rss_replace(msg)
			msg = rss_del_nn(msg)

			if submode == 'body' or submode == 'head':
				msg = msg[:-1]

#			writefile('settings/tmpfeed',str(msg))

			msg = msg[:-1]
			if lng > 1 and submode == 'full':
				msg = msg[:-1]
		else:
			msg = u'bad url or rss not found!'

#---------

	elif mode == 'del':
		link = text[1]
		if link[:7] != 'http://':
        	        link = 'http://'+link

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

		if bedel1 or bedel2:
			msg = u'Delete feed from schedule: '+link
		if bedel1:
			writefile(feeds,str(feedbase))
		if bedel2:
			writefile(lafeeds,str(lastfeeds))
		else:
			msg = u'Can\'t find in schedule: '+link

	elif mode == 'new' or mode == 'get':
	        link = text[1]
       		if link[:7] != 'http://':
        	        link = 'http://'+link
        	f = urllib.urlopen(link)
        	feed = f.read()
		f.close()

		is_atom = feed[:100].count('http://www.w3.org/2005/Atom') and feed[:100].count('xml')
		is_rss = feed[:100].count('rss') and feed[:100].count('xml')

		if is_atom or is_rss:
			encidx = feed.find('encoding=')
			if encidx >= 0:
				enc = feed[encidx+10:encidx+30]
				enc = enc[:enc.index('?>')-1]
				enc = enc.upper()
			else:
				enc = 'UTF-8'
		
	        	feed = unicode(feed, enc)
			if is_rss:
		        	feed = feed.split('<item>')
			if is_atom:
		        	feed = feed.split('<entry>')
	        	msg = 'Feeds for '+link+' '
	
	        	if len(text) > 2:
	        	        lng = int(text[2])+1
	        	else:
	        	        lng = len(feed)
	        	        
	        	if len(feed) <= lng:
	        	        lng = len(feed)
	        	if lng>=11:
	        	        lng = 11

	        	if len(text) > 3:
	        	        submode = text[3]
	        	else:
	        	        submode = 'full'


			tstop = ''
			for ii in lastfeeds:
				if ii[2] == jid and ii[0] == link:
					 tstop = ii[1]
					 tstop = tstop[:-1]

			mmsg = feed[0]
	                msg += mmsg[mmsg.index('<title>')+7:mmsg.index('</title>')]+ '\n'
			mmsg = feed[1]
			if is_rss:
				mmsg = mmsg[mmsg.index('<title>')+7:mmsg.index('</title>')]+ '\n'
			if is_atom:
				mmsg = mmsg[mmsg.find('>',mmsg.index('<content'))+1:mmsg.index('</content>')]+ '\n'
			for dd in lastfeeds:
                                if dd[0] == link and dd[2] == jid:
                                        lastfeeds.remove(dd)
			lastfeeds.append([link,mmsg,jid])
			writefile(lafeeds,str(lastfeeds))

	        	for idx in range(1,lng):
                                over = idx
	        	        mmsg = feed[idx]
				if is_rss:
					ttitle = mmsg[mmsg.index('<title>')+7:mmsg.index('</title>')]
					tbody = mmsg[mmsg.index('<description>')+13:mmsg.index('</description>')]
				if is_atom:
					ttitle = mmsg[mmsg.find('>',mmsg.index('<content'))+1:mmsg.index('</content>')]
					tbody = mmsg[mmsg.find('>',mmsg.index('<title'))+1:mmsg.index('</title>')]

                                if mode == 'new':
        				if ttitle == tstop:
        					break
				if submode == 'full':
		        	        msg += u' • ' + ttitle + '\n'
					msg += tbody + '\n\n'
				elif submode == 'body':
					msg += tbody + '\n'
				elif submode[:4] == 'head':
		        	        msg += u' • ' + ttitle+ '\n'

                        if mode == 'new':
        		        if over == 1 and text[4] == 'silent':
                                        nosend = 1
                                elif over == 1 and text[4] != 'silent':
                                        msg = 'New feeds not found! '

			if submode == 'body' or submode == 'head':
				msg = msg[:-1]

			msg = rss_replace(msg)
			msg = rss_del_html(msg)
			msg = rss_replace(msg)
			msg = rss_del_nn(msg)

			msg = msg[:-1]

			if lng > 1 and submode == 'full':
				msg = msg[:-1]


		else:
			msg = u'bad url or rss not found!'
        if not nosend:
		send_msg(type, jid, nick, msg)
	

#------------------------------------------------

# в начале
# 0 - всем
# 1 - админам\овнерам
# 2 - владельцу бота

# в конце
# 0 - передавать параметры
# 1 - ничего не передавать
# 2 - передавать остаток текста

comms = [(1, prefix+u'stats', stats, 1),
	 (1, prefix+u'gstats', gstats, 1),
         (2, prefix+u'quit', bot_exit, 2),
         (2, prefix+u'restart', bot_restart, 2),
         (2, prefix+u'update', bot_update, 2),
         (1, prefix+u'say', say, 2),
         (1, prefix+u'age', true_age, 2),
         (2, prefix+u'gsay', gsay, 2),
         (0, prefix+u'help', helpme, 2),
         (2, prefix+u'join', bot_join, 2),
         (2, prefix+u'leave', bot_leave, 2),
         (2, prefix+u'rejoin', bot_rejoin, 2),
         (2, prefix+u'pass', conf_pass, 2),
         (2, prefix+u'owner', owner, 2),
         (2, prefix+u'ignore', ignore, 2),
         (1, prefix+u'where', info_where, 1),
         (1, prefix+u'res', info_res, 2),
         (1, prefix+u'serv', info_serv, 2),
         (0, prefix+u'inbase', info_base, 1),
         (2, prefix+u'search', info_search, 2),
         (1, prefix+u'look', real_search, 2),
         (1, prefix+u'tempo', tmp_search, 2),
         (2, prefix+u'gtempo', gtmp_search, 2),
         (1, prefix+u'rss', rss, 2),
         (1, prefix+u'youtube', youtube, 2),
         (0, prefix+u'wzcity', weather_city, 2),
         (1, prefix+u'wzz', weather_raw, 2),
         (0, prefix+u'wz', weather, 2),
         (1, prefix+u'commands', info_comm, 1),
         (1, prefix+u'uptime', uptime, 1),
         (1, prefix+u'info', info, 1),
         (1, prefix+u'smile', smile, 1),
         (1, prefix+u'inban', inban, 2),
#        (2, prefix+u'log', get_log, 2),
         (2, prefix+u'limit', conf_limit, 2),
         (2, prefix+u'plugin', bot_plugin, 2),
         (1, prefix+u'def', defcode, 2),
         (2, prefix+u'error', show_error, 2),
         (0, prefix+u'whoami', info_access, 1),
	 (2, prefix+u'prefix', set_prefix, 2),
         (1, prefix+u'clear', hidden_clear, 1)]
