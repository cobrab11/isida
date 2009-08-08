#!/usr/bin/python
# -*- coding: utf -*-

def getMucItems(jid,affil,ns):
	global banbase,raw_iq
	iqid = str(randint(1,100000))
	raw_iq = []
	if ns == NS_MUC_ADMIN: i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':affil})])])
	else: i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': ns},[])])
	cl.send(i)
	while not banbase.count((u'TheEnd', u'None', iqid)): sleep(0.1)
	bb = []
	for b in banbase: 
		if b[2] == iqid and b[0] != u'TheEnd': bb.append(b)
	for b in banbase:
		if b[2] == iqid: banbase.remove(b)
	return (bb,raw_iq)

def conf_backup(type, jid, nick, text):
	if len(text):
		text = text.split(' ')
		mode = text[0]

		if mode == u'show':
			a = os.listdir(back_folder)
			b = []
			for c in a:
				if c.count('conference'): b.append((c,os.path.getmtime(back_folder+c)))
			if len(b):
				msg = u'Резервные копии: '
				for c in b: msg += c[0]+' ('+un_unix(time.time()-c[1])+')'+', '
				msg = msg[:-2]
			else: msg = u'Резервных копий не найдено!'
		if mode == u'now':
			tmppos = arr_semi_find(confbase, jid)
			if tmppos == -1:
				nowname = nickname
			else:
				nowname = getResourse(confbase[tmppos])
				if nowname == '':
					nowname = nickname
			xtype = ''
			for base in megabase:
				if base[0].lower() == jid and base[1] == nowname:
					xtype = base[3]
					break
			if xtype != 'owner': msg = u'Для резервного копирования мне нужны права владельца конференции!'

			else:
				ns = NS_MUC_ADMIN
				banlist = getMucItems(jid,'outcast',ns)
				memberlist = getMucItems(jid,'member',ns)
				adminlist = getMucItems(jid,'admin',ns)
				ownerlist = getMucItems(jid,'owner',ns)
				configlist = getMucItems(jid,'',NS_MUC_OWNER)
				iqid = str(randint(1,100000))
				i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'admin', 'jid':getRoom(str(selfjid))},[])])])
				cl.send(i)

				msg = u'Копирование завершено!'
				msg += u'\nВладельцев:\t'+str(len(ownerlist[0]))
				msg += u'\nАдминов:\t'+str(len(adminlist[0]))
				msg += u'\nУчастников:\t'+str(len(memberlist[0]))
				msg += u'\nЗабаненных:\t'+str(len(banlist[0]))

				raw_back = []
				raw_back.append(ownerlist[1][1])
				raw_back.append(adminlist[1][1])
				raw_back.append(memberlist[1][1])
				raw_back.append(banlist[1][1])
				raw_back.append(configlist[1][1])
				writefile(back_folder+unicode(jid),str(raw_back))

		if mode == u'restore':
			if len(text)>1:
				a = os.listdir(back_folder)
				a = a.count(text[1])

				if a:
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
					if xtype != 'owner': msg = u'Для восстановления резервной копии мне нужны права владельца конференции!'
					else:
						raw_back=eval(readfile(back_folder+unicode(text[1])))
						for zz in range(0,4):
							iqid = str(randint(1,100000))
							end = raw_back[zz][raw_back[zz].find('<query'):]
							beg = '<iq xmlns="jabber:client" to="'+str(jid)+'" from="'+str(selfjid)+'" id="'+str(iqid)+'" type="set">'
							cl.send(beg+end)
						iqid = str(randint(1,100000))
						end = raw_back[4][raw_back[4].find('<query'):]
						beg = '<iq to="'+str(jid)+'" id="'+str(iqid)+'" type="set">'
						i = beg+end
						ci = i.count('label="')
						for ii in range(0,ci): i = i[:i.find('label="')-1]+i[i.find('"',i.find('label="')+8)+1:]
						i = i[:i.find('<instructions>')]+i[i.find('</instructions>',i.find('<instructions>')+14)+15:]
						i = i[:i.find('<title>')]+i[i.find('</title>',i.find('<title>')+7)+8:]
						i = i.replace('form','submit')
						cl.send(i)
						iqid = str(randint(1,100000))
						i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'admin', 'jid':getRoom(str(selfjid))},[])])])
					cl.send(i)
					msg = u'Восстановление завершено!'
				else: msg = u'Резервная копия не найдена. Просмотрите список используя ключ show'
			else: msg = u'Что будем восстанавливать?'
	else: msg = u'backup now|show|restore'
	send_msg(type, jid, nick, msg)

global execute

execute = [(1, u'backup', conf_backup, 2, u'Резервное копирование/восстановление конференций.\nbackup show|now|restore\nshow - показать доступные копии\nnow - сохронить текущую конференцию\nrestore название_конференции - восстановить конференцию в текущей')]
