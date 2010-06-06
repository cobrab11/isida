#!/usr/bin/python
# -*- coding: utf -*-

def getMucItems(jid,affil,ns):
	global banbase,raw_iq,iq_request
	iqid = get_id()
	raw_iq = []
	if ns == NS_MUC_ADMIN: i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':affil})])])
	else: i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': ns},[])])
	iq_request[iqid]=(time.time(),'','')
	sender(i)
	while not banbase.count(('TheEnd', 'None', iqid)): sleep(backup_sleep_time)
	iq_request.pop(iqid)
	bb,cc = [],[]
	for b in banbase: 
		if b[2] == iqid:
			if b[0] != 'TheEnd': bb.append(b)
		else: cc.append(b)
	banbase = cc
	return (bb,raw_iq)

def conf_backup(type, jid, nick, text):
	if len(text):
		text = text.split(' ')
		mode = text[0]

		if mode == 'show':
			a = os.listdir(back_folder)
			b = []
			for c in a:
				if c.count('conference'): b.append((c,os.path.getmtime(back_folder+c)))
			if len(b):
				msg = L('Available copies:') + ' '
				for c in b: msg += c[0]+' ('+un_unix(time.time()-c[1])+')'+', '
				msg = msg[:-2]
			else: msg = L('Backup copies not found.')
		if mode == 'now':
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
			if xtype != 'owner': msg = L('I need an owner affiliation for backup settings!')

			else:
				ns = NS_MUC_ADMIN
				banlist = getMucItems(jid,'outcast',ns)
				memberlist = getMucItems(jid,'member',ns)
				adminlist = getMucItems(jid,'admin',ns)
				ownerlist = getMucItems(jid,'owner',ns)
				configlist = getMucItems(jid,'',NS_MUC_OWNER)
				iqid = get_id()
				i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'admin', 'jid':getRoom(str(selfjid))},[])])])
				sender(i)

				msg = L('Copying completed!\nOwners:\t%s\nAdmins:\t%s\nMembers:\t%s\nBanned:\t%s') % (str(len(ownerlist[0])),\
					str(len(adminlist[0])), str(len(memberlist[0])), str(len(banlist[0])))
				raw_back = []
				raw_back.append(ownerlist[1][1])
				raw_back.append(adminlist[1][1])
				raw_back.append(memberlist[1][1])
				raw_back.append(banlist[1][1])
				raw_back.append(configlist[1][1])
				writefile(back_folder+unicode(jid),unicode(raw_back))

		if mode == 'restore':
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
					if xtype != 'owner': msg = L('I need an owner affiliation for restore settings!')
					else:
						raw_back=eval(readfile(back_folder+unicode(text[1])))
						for zz in range(0,4):
							iqid = get_id()
							end = raw_back[zz][raw_back[zz].find('<query'):]
							beg = '<iq xmlns="jabber:client" to="'+unicode(jid)+'" from="'+unicode(selfjid)+'" id="'+unicode(iqid)+'" type="set">'
							i = beg+end
							sender(i)
							sleep(i.count('<item')*0.02)
						iqid = get_id()
						end = raw_back[4][raw_back[4].find('<query'):]
						beg = '<iq to="'+unicode(jid)+'" id="'+unicode(iqid)+'" type="set">'
						i = beg+end
						while i.count(' label="'): i = i[:i.find(' label="')]+i[i.find('"',i.find(' label="')+8)+1:]
						while i.count('<option>') and i.count('</option>'): i = i.replace(get_tag_full(i,'option'),'')
						i = i.replace('<value />','<value></value>')
						i = i.replace('<value/>','<value></value>')
						i = i[:i.find('<instructions>')]+i[i.find('</instructions>',i.find('<instructions>')+14)+15:]
						i = i[:i.find('<title>')]+i[i.find('</title>',i.find('<title>')+7)+8:]
						i = i.replace('form','submit')
						sender(i)
						sleep(backup_sleep_time)
						iqid = get_id()
						i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'admin', 'jid':getRoom(unicode(selfjid))},[])])])
						sleep(backup_sleep_time)
						sender(i)
						sleep(backup_sleep_time)
						msg = L('Restore completed.')
				else: msg = L('Copy not found. Use key "show" for lisen available copies.')
			else: msg = L('What do you want to restore?')
	else: msg = 'backup now|show|restore'
	send_msg(type, jid, nick, msg)

global execute

execute = [(8, 'backup', conf_backup, 2, L('Backup/restore conference settings.\nbackup show|now|restore\nshow - show available copies\nnow - backup current conference\nrestore name_conference - restore settings name_conference in current conference'))]
