#!/usr/bin/python
# -*- coding: utf -*-

def disco(type, jid, nick, text):
	if text == '':
		send_msg(type, jid, nick, u'Ась?')
		return
	text = text.lower().split(' ')
	where = text[0]
	try: what = text[1]
	except: what = ''
	try: hm = int(text[2])
	except: hm = 10

	iqid = str(randint(1,100000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':where}, payload = [Node('query', {'xmlns': NS_DISCO_ITEMS},[])])
	cl.send(i)
	to = timeout

	no_answ, is_answ = 1, None
	while to >= 0 and no_answ:
		for aa in iq_answer:
			if aa[0]==iqid:
				is_answ = aa[1:]
				iq_answer.remove(aa)
				no_answ = 0
				break
		sleep(0.5)
		to -= 0.5

	if not no_answ and is_answ[0] != None:
		if where.count('conference') and not where.count('@'):
			tmp = sqlite3.connect(':memory:')
			cu = tmp.cursor()
			cu.execute('''create table tempo (nick text, room text, size text)''')
			isa = is_answ[0].split('<item ')
			for ii in isa[1:]:
				dname = get_subtag(ii,'name')
				djid = get_subtag(ii,'jid')
				dpos = 1
				for zzz in range(0,dname.count('(')):
					dpos = dname.find('(',dpos+1)
				dsize = dname[dpos+1:dname.find(')',dpos+1)]
				dname = dname[:-(len(dsize)+3)]
				cu.execute('insert into tempo values (?,?,?)', (dname, djid, dsize))
			if len(what):
				cm = cu.execute('select * from tempo where (nick like ? or room like ?) order by -size',('%'+what+'%','%'+what+'%')).fetchmany(hm)
			else:
				cm = cu.execute('select * from tempo order by -size').fetchmany(hm)
			if len(cm):
				cnt = 1
				msg = u'Всего: '+str(len(cm))
				for i in cm:
					msg += u'\n'+str(cnt)+u'. '+i[0]+u' ['+i[1]+u'] . '+i[2]
					cnt += 1
			else:
				msg = u'\"'+what+u'\" не найдено!'
			tmp.close()
		elif where.count('conference') and where.count('@'):
			tmp = sqlite3.connect(':memory:')
			cu = tmp.cursor()
			cu.execute('''create table tempo (nick text)''')
			isa = is_answ[0].split('<item ')
			for ii in isa[1:]:
				dname = get_subtag(ii,'name')
				cu.execute('insert into tempo values (?)', (dname,))
			if len(what):
				cm = cu.execute('select * from tempo where (nick like ?) order by nick',('%'+what+'%',)).fetchall()
			else:
				cm = cu.execute('select * from tempo order by nick').fetchall()
			if len(cm):
				msg = u'Всего: '+str(len(cm))+' - '
				for i in cm:
					msg += i[0]+u', '
				msg = msg[:-2]
			else:
				msg = u'\"'+what+u'\" не найдено!'
			tmp.close()
		else:
			tmp = sqlite3.connect(':memory:')
			cu = tmp.cursor()
			cu.execute('''create table tempo (jid text)''')
			isa = str(is_answ[0]).split('<item ')
			for ii in isa[1:]:
				djid = get_subtag(ii,'jid')
				cu.execute('insert into tempo values (?)', (djid,))
			cm = cu.execute('select * from tempo order by jid').fetchall()
			if len(cm):
				cnt = 1
				msg = u'Всего: '+str(len(cm))
				for i in cm:
					msg += '\n'+str(cnt)+'. '+i[0]
					cnt += 1
			else:
				msg = u'не найдено!'
			tmp.close()
	else:
		msg = u'Не получается...'
	msg = rss_replace(msg)
	send_msg(type, jid, nick, msg)

def whereis(type, jid, nick, text):
	if len(text):
		text = text.split(' ')
		who = text[0]
	else:
		who = nick
	if len(text)<2:
		where = getServer(jid)
	else:
		if text[1].count('conference'):
			where = text[1]
		else:
			where = 'conference.'+text[1]
	iqid = str(randint(1,100000))
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':where}, payload = [Node('query', {'xmlns': NS_DISCO_ITEMS},[])])
	cl.send(i)
	to = timeout

	no_answ = 1
	while to >= 0 and no_answ:
		for aa in iq_answer:
			if aa[0]==iqid:
				is_answ = aa[1:]
				iq_answer.remove(aa)
				no_answ = 0
				break
		sleep(0.5)
		to -= 0.5

	if not no_answ:
		tmp = sqlite3.connect(':memory:')
		cu = tmp.cursor()
		cu.execute('''create table tempo (nick text, room text)''')

		isa = is_answ[0].split('<item ')
		djids = []
		for ii in isa[1:]:
			dname = get_subtag(ii,'name')
			if dname[-5:] != '(n/a)' and dname[-3:] != '(0)':
				djids.append(get_subtag(ii,'jid'))

		send_msg(type, jid, nick, u'Ожидайте, результат Вы получите в приват примерно через '+str(int(len(djids)/6))+u' сек.')

		for ii in djids:
			iqid = str(randint(1,100000))
			i = Node('iq', {'id': iqid, 'type': 'get', 'to':ii}, payload = [Node('query', {'xmlns': NS_DISCO_ITEMS},[])])
			cl.send(i)
			to = 500

			no_answ = 1
			while to >= 0 and no_answ:
				for aa in iq_answer:
					if aa[0]==iqid:
						is_answ = aa[1:]
						iq_answer.remove(aa)
						no_answ = 0
						break
				sleep(0.01)
				to -= 0.01

			if not no_answ:
				isd = is_answ[0].split('<item ')
				for iii in isd[1:]:
					dname = get_subtag(iii,'name')
					if dname.lower().count(who.lower()):
						cu.execute('insert into tempo values (?,?)', (dname, getRoom(get_subtag(iii,'jid'))))

		cm = cu.execute('select * from tempo order by nick,room').fetchall()
		if len(cm):
			msgg = u', Совпадений с ником \"'+who+u'\": '+str(len(cm))
			for i in cm:
				msgg += '\n'+i[0]+'\t'+i[1]
		else:
			msgg = u', ник \"'+who+u'\" не найден!'

		msg = u'Всего конференций: '+str(len(isa)-1)+u', доступно: '+str(len(djids))+msgg
		tmp.close()		
	else:
		msg = u'Не получается...'
	send_msg('chat', jid, nick, msg)

global execute

execute = [(0, u'disco', disco, 2, u'Обзор сервисов.\ndisco server.tld - запрос информации о сервере\ndisco conference.server.tld [body [size]] - поиск строки body в обзоре конференций и показ size результатов\ndisco room@conference.server.tld [body [size]] - поиск строки body в обзоре конференции room и показ size результатов'),
	 (1, u'whereis', whereis, 2, u'Поиск ника по серверу конференций\nwhereis - поиск своего ника по серверу на котором находится текущая конференция\nwhereis nick - поиск ника по серверу на котором находится текущая конференция\nwhereis nick [conference.]server.tld - поиск ника по серверу server.tld')]
