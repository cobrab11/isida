# -*- coding: utf -*-

def info_comm(type, jid, nick):
	global comms
	msg = ''
	ccnt = 0
	for ccomms in comms:
		if not ccomms[1].count(god):
			msg += ccomms[1]+'('+str(ccomms[0])+'), '
			ccnt += 1
	msg = msg[:-2]
	msg = u'Команды парсера: '+str(ccnt)+'\n'+msg+u'\nДоступ: 0 - всем, 1 - админам/овнерам, 2 - владельцу бота'
	send_msg(type, jid, nick, msg)

def test(type, jid, nick):
	send_msg(type, jid, nick, 'passed')

def test_rus(type, jid, nick):
	send_msg(type, jid, nick, u'две полоски!')
        
def no_spam(type, jid, nick):
	send_msg(type, jid, nick, u'Куй тебе по всей морде!')

def bot_exit(type, jid, nick, text):
        text = text[0]
	StatusMessage = 'Exit by command from bot owner ('+nick+')'
	send_presence_all(StatusMessage)
	sleep(5)
	os._exit(0)

def say(type, jid, nick, text):
	send_msg(type, jid, nick, text)

def helpme(type, jid, nick, text):
	pprint(text)
	helps = [(u'search',u'Поиск по внутренней базе jid\'ов'),
		(u'tempo',u'Поиск по временной базе ролей/аффиляций'),
		(u'owner',u'Изменение владельцев бота:\nowner add nick - добавить ник в список\nowner del nick - удалить ник из списка\nowner clr - быстрая очистка списка'),
		(u'info',u'Основная инфа о боте'),
		(u'where',u'Список конференций, в которых находится бот'),
		(u'res',u'топ10 рессурсов. Возможен поиск через res text'),
		(u'serv',u'Список серверов, которые бот видел. Возможен поиск через serv text'),
		(u'test',u'хз что это...'),
		(u'тест',u'хз что это...'),
		(u'join',u'Вход в конфу.\njoin room - зайти в конфу room на последнем активном сервере и с последним активным ником\njoin 	room@conference.server.ru - зайти в конфу с последним активным ником\njoin room@conference.server.ru/nick - зайти в конфу'),
		(u'leave',u'Выход из конфы.\nleave [room@conference.server.ru] - если не указанна конфа, то выход из текущей конфы.'),
		(u'quit',u'Завершение работы бота'),
		(u'clear',u'Скрытая очистка истории сообщений'),
		(u'pass',u'Установка пароля для входа в конфу'),
		(u'rss',u'Каналы новостей:\nrss show\nrss add url time [full|body|headers]\nrss del url\nrss now url [количество] [full|body|headers]\n')]

# show | add | del | clr | now | get

	mesg = u'Доступна справка по командам:\n'
	for hlp in helps:
		mesg += hlp[0] + ', '
	mesg = mesg[:-2]
	for hlp in helps:
		if text.lower() == hlp[0]:
			mesg = hlp[1]
	send_msg(type, jid, nick, mesg)

def hidden_clear(type, jid, nick):
        pprint(u'clear: '+unicode(jid)+u' by: '+unicode(nick))
        cntr = 19                
        while (cntr>0):
                cl.send(xmpp.Message(jid, '', "groupchat"))
                time.sleep(1.05)
                cntr=cntr-1
        send_msg(type, jid, nick, u'стирильно!!!')

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
        global confs, confbase
        if len(confbase) == 1:
                send_msg(type, jid, nick, u'не могу выйти из последней конфы!')
        else:
                if len(text):
                        text=unicode(text)
                else:
                        text=jid
                lroom = text
                                
		if arr_semi_find(confbase, lroom) >= 0:
#                if confbase.count(lroom):
#                        confbase.remove(lroom)
			confbase = arr_del_semi_find(confbase,lroom)
                        writefile(confs,str(confbase))
                        send_msg(type, jid, nick, u'свалила из '+text)
			sm = u'Меня выводит '+nick
                        leaveconf(text, domain, sm)
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
        global lfrom, lto
        text=unicode(text)
        if text!='':
		text = text.split(' ')
                lfrom = int(text[0])
		lto = int(text[1])
        send_msg(type, jid, nick, u'limit from '+str(lfrom)+' to '+str(lto))

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
        elif do == 'clr':
                ownerbase = [god]

	msg = u'Я принимаю команды от: '
	for jjid in ownerbase:
			msg += jjid+', '
	msg = msg[:-2]
	writefile(owners,str(ownerbase))
        send_msg(type, jid, nick, msg)

def info_where(type, jid, nick):
        global confbase
        msg = u'Активных конференций: '+str(len(confbase))+'\n'
        for jjid in confbase:
                msg += jjid+', '
        msg = msg[:-2]
        send_msg(type, jid, nick, msg)

def info(type, jid, nick):
        global confbase        
        msg = u'Активных конференций: '+str(len(confbase))+u' (подробнее where)\n'
        msg += u'Активный сервер: '+lastserver+'\n'
        msg += u'Активный ник: '+lastnick
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


def tmp_search(type, jid, nick, text):
        msg = u'Чего искать то будем?'
	if text != '':
        	msg = u'Найдено:'
                fl = 1
                for mega1 in megabase:
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

#[room, nick, role, affiliation, jid]

feeds = 'feed'

def rss(type, jid, nick, text):
        text = text.split(' ')
	mode = text[0] # show | add | del | clr | now | get

	if os.path.isfile(feeds):
		feedbase = eval(readfile(feeds))
	else:
		feedbase = []
		writefile(feeds,str(feedbase))

	if mode == 'show':
		msg = 'Feeds shelude:'
		for rs in feedbase:
			msg += u'\n'+rs[0]+u' ('+rs[1]+u') '+rs[2]
			lt = rs[3]
			msg += u' '+str(lt[2])+u'.'+str(lt[1])+u'.'+str(lt[0])+u' '+str(lt[3])+u':'+str(lt[4])+u':'+str(lt[5])

	elif mode == 'add':
		lt=localtime()
		link = text[1]
		if link[:7] != 'http://':
        	        link = 'http://'+link
		feedbase.append([link, text[2], text[3], lt[:6]]) # url time mode
		msg = u'Add feed to shelude: '+link+u' ('+text[2]+u') '+text[3]
		writefile(feeds,str(feedbase))
	elif mode == 'del':
		link = text[1]
		if link[:7] != 'http://':
        	        link = 'http://'+link

		bedel = 0
		for rs in feedbase:
			if rs[0] == link:
				feedbase.remove(rs)
				bedel = 1
		if bedel:
			msg = u'Delete feed from shelude: '+link
			writefile(feeds,str(feedbase))
		else:
			msg = u'Can\'t find in shelude: '+link

	elif mode == 'now':
	        link = text[1]
       		if link[:7] != 'http://':
        	        link = 'http://'+link
        	f = urllib.urlopen(link)
        	feed = f.read()

		writefile('tempofeed',str(feed))
		if feed[:100].count('rss') and feed[:100].count('xml'):
			encidx = feed.index('encoding=')
			enc = feed[encidx+10:encidx+30]
			enc = enc[:enc.index('?>')-1]
			enc = enc.upper()
		
	        	feed = unicode(feed, enc)
	        	feed = feed.split('<item>')
	        	msg = 'Feeds for '+link+' '
	
	        	if len(text) > 2:
	        	        lng = int(text[2])
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
        	        
			mmsg = feed[0]
	                msg += mmsg[mmsg.index('<title>')+7:mmsg.index('</title>')]+ '\n'
			
	        	for idx in range(1,lng):
	        	        mmsg = feed[idx]
				if submode == 'full':
		        	        msg += mmsg[mmsg.index('<title>')+7:mmsg.index('</title>')]+ '\n'
					msg += mmsg[mmsg.index('<description>')+13:mmsg.index('</description>')] + '\n\n'
				elif submode == 'body':
					msg += mmsg[mmsg.index('<description>')+13:mmsg.index('</description>')] + '\n'
				elif submode[:4] == 'head':
		        	        msg += mmsg[mmsg.index('<title>')+7:mmsg.index('</title>')]+ '\n'
	
			msg = msg.replace('<br>','\n')
			msg = msg.replace('<br />','\n')
			msg = msg.replace('<br/>','\n')
			msg = msg.replace('<![CDATA[','')
			msg = msg.replace(']]>','')
			msg = msg.replace('&lt;','<')
			msg = msg.replace('&gt;','>')
			msg = msg.replace('&quot;','\"')
			msg = msg.replace('&amp;','&')
			if submode == 'full':
				msg = msg[:-2]
			else:
				msg = msg[:-1]
		else:
			msg = u'bad url or rss not found!'

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

comms = [(0, u'test', test, 1),
         (0, u'тест', test_rus, 1),
         (1, u'spam '+god, no_spam, 1),
         (2, u'quit', bot_exit, 0, u'Завершаю работу'),
         (1, u'say', say, 2),
         (0, u'help', helpme, 2),
         (2, u'join', bot_join, 2),
         (2, u'leave', bot_leave, 2),
         (2, u'pass', conf_pass, 2),
         (2, u'owner', owner, 2),
         (1, u'where', info_where, 1),
         (1, u'res', info_res, 2),
         (1, u'serv', info_serv, 2),
         (2, u'base', info_base, 1),
         (1, u'search', info_search, 2),
         (1, u'tempo', tmp_search, 2),
         (0, u'rss', rss, 2),
         (1, u'commands', info_comm, 1),
         (2, u'info', info, 1),
         (1, u'clear', hidden_clear, 1)]
