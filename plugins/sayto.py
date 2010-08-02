#!/usr/bin/python
# -*- coding: utf -*-

last_cleanup_sayto_base = 0

def sayto(type, jid, nick, text):
	if text.split(' ')[0] == 'show':
		try: text = text.split(' ',1)[1]
		except: text = ''
		ga = get_level(jid, nick)
		if ga[0] != 9: msg = L('You access level is to low!')
		else:
			sdb = sqlite3.connect(saytobase)
			cu = sdb.cursor()
			cm = cu.execute('select * from st').fetchall()
			if len(cm):
				msg = ''
				for cc in cm:
					zz = cc[0].split('\n')
					tmsg = '\n' + cc[1] +'/'+ zz[0] +' ('+un_unix(time.time()-int(zz[1]))+'|'+un_unix(GT('sayto_timeout')-(time.time()-int(zz[1])))+') '+L('for')+' '+cc[2]+' - '+cc[3]
					if len(text) and tmsg.lower().count(text.lower()): msg += tmsg
					elif not len(text): msg += tmsg
				if len(msg): msg = L('Not transfered messages: %s') % msg
				else: msg = L('Not found!')
				if type == 'groupchat':
					send_msg('chat', jid, nick, msg)
					msg = L('Sent in private message')
			else: msg = L('List is empty.')
	elif text.count(' '):
		to = text.split(' ')[0]
		what = text.split(' ',1)[1]
		frm = nick + '\n' + str(int(time.time()))
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		fnd = cu.execute('select status, jid from age where room=? and nick=? group by jid',(jid,to)).fetchall()
		if len(fnd) == 1:
			fnd = fnd[0]
			if fnd[0]:
				msg = L('I will convey your message.')
				sdb = sqlite3.connect(saytobase)
				cu = sdb.cursor()
				cu.execute('insert into st values (?,?,?,?)', (frm, jid, fnd[1], what))
				sdb.commit()
			else: msg = L('Or am I a fool or %s is here.') % to
		elif len(fnd) > 1:
			off_count = 0
			sdb = sqlite3.connect(saytobase)
			cu = sdb.cursor()
			for tmp in fnd:
				if tmp[0]:
					cu.execute('insert into st values (?,?,?,?)', (frm, jid, tmp[1], what))
					off_count += 1
			sdb.commit()
			if off_count: msg = L('I seen some people with this nick, and I can convey is incorrect. Coincidence: %s, and count convey messages: %s') % (str(len(fnd)), str(off_count))
			else: msg = L('All people with this nickname are here!')
		else:
			if to.count('@') and to.count('.'):
				fnd = cu.execute('select status, jid from age where room=? and jid=? group by jid',(jid,to)).fetchall()
				sdb = sqlite3.connect(saytobase)
				cu = sdb.cursor()
				if fnd:
					off_count = 0
					for tmp in fnd:
						if tmp[0]:
							cu.execute('insert into st values (?,?,?,?)', (frm, jid, tmp[1], what))
							off_count += 1
					if off_count: msg = L('I will convey your message.')
					else: msg = L('This jid is here!')
				else:
					msg = L('I didn\'t seen user with jid %s, but if he join here I convey your message.') % to
					cu.execute('insert into st values (?,?,?,?)', (frm, jid, to, what))
				sdb.commit()
			else: msg = L('I didn\'t see user with nick %s. You can use jid.') % to
	else: msg = L('What convey to?')
	send_msg(type, jid, nick, msg)

def sayto_presence(room,jid,nick,type,text):
	if nick != '':
		sdb = sqlite3.connect(saytobase)
		cu = sdb.cursor()
		cm = cu.execute('select * from st where room=? and (jid=? or jid=?)',(room, getRoom(jid), nick)).fetchall()
		if len(cm):
			cu.execute('delete from st where room=? and (jid=? or jid=?)',(room, getRoom(jid), nick))
			for cc in cm:
				if cc[0].count('\n'):
					zz = cc[0].split('\n')
					send_msg('chat', room, nick, L('%s (%s ago) convey for you: %s') % (zz[0], un_unix(time.time()-int(zz[1])), cc[3]))
				else: send_msg('chat', room, nick, L('%s convey for you: %s') % (cc[3], cc[0]))
			sdb.commit()

def cleanup_sayto_base():
	global last_cleanup_sayto_base
	ctime = int(time.time())
	if ctime-last_cleanup_sayto_base > GT('sayto_cleanup_time'):
		last_cleanup_sayto_base = ctime
		sdb = sqlite3.connect(saytobase)
		cu = sdb.cursor()
		cm = cu.execute('select who, room, jid from st').fetchall()
		if len(cm):
			for cc in cm:
				if cc[0].count('\n'):
					tim = int(cc[0].split('\n')[1])
					if ctime-tim > GT('sayto_timeout'): cu.execute('delete from st where room=? and jid=?',(cc[1], cc[2]))
				else: cu.execute('delete from st where room=? and jid=?',(cc[1], cc[2]))
			sdb.commit()

def sayjid(type, jid, nick, text):
	try:
		text = text.split(' ',1)
		if len(text) != 2: msg = L('Error!')
		elif not text[0].count('@') and not text[0].count('@'): msg = L('Error!')
		elif not len(text[1]): msg = L('Error!')
		else: 
			send_msg(type, jid, nick, L('Sent'))
			msg = L('%s from conference %s convey message for you: %s') % (nick, jid, text[1])
			type, nick, jid = 'chat', '', text[0]
	except: msg = L('Error!')
	send_msg(type, jid, nick, msg)
			
global execute, timer, presence_control

timer = [cleanup_sayto_base]
presence_control = [sayto_presence]
execute = [(3, 'sayto', sayto, 2, L('"Say to" command.\nsayto jid|nick message - if jid or nick join in conference, bot send "message". Messages saves 14 days, after if message didn\'t be send this message remove.')),
			(7, 'sayjid', sayjid, 2, L('Send message to jid\n sayjid jid message.'))]
