#!/usr/bin/python
# -*- coding: utf -*-

def true_age_split(type, jid, nick, text):
	true_age_raw(type, jid, nick, text, True)

def true_age(type, jid, nick, text):
	true_age_raw(type, jid, nick, text, None)
	
def true_age_raw(type, jid, nick, text, xtype):
	while text[-1:] == ' ': text = text[:-1]
	text = text.split('\n')
	llim = 10
	if len(text)>=2:
		try: llim = int(text[1])
		except: llim = GT('age_default_limit')
	text = text[0]
	if text == '': text = nick
	if llim > GT('age_max_limit'): llim = GT('age_max_limit')
	mdb = sqlite3.connect(agestatbase,timeout=base_timeout)
	cu = mdb.cursor()
	real_jid = cu.execute('select jid from age where room=? and (nick=? or jid=?) order by -time,-status',(jid,text,text.lower())).fetchone()
	if not real_jid:
		text = '%'+text.lower()+'%'
		real_jid = cu.execute('select jid from age where room=? and (nick like ? or jid like ?) order by -time,-status',(jid,text,text)).fetchone()		
	try:
		if xtype: sbody = cu.execute('select * from age where room=? and jid=? order by -time,-status',(jid,real_jid[0])).fetchmany(llim)
		else:
			t_age = cu.execute('select sum(age) from age where room=? and jid=? order by -time,-status',(jid,real_jid[0])).fetchone()
			sbody = cu.execute('select * from age where room=? and jid=? order by -time,-status',(jid,real_jid[0])).fetchone()
			sbody = [sbody[:4] + t_age + sbody[5:]]
	except: sbody = None
	if sbody:
		msg = L('I see:')
		cnt = 1
		for tmp in sbody:
			if tmp[5]: r_age = tmp[4]
			else: r_age = int(time.time())-tmp[3]+tmp[4]
			if xtype: msg += '\n'+str(cnt)+'. '+tmp[1]
			else: msg += ' '+tmp[1]
			msg += '\t'+un_unix(r_age)+', '

			if tmp[5]:
				if tmp[6] != '': msg += L('%s %s ago') % (tmp[6],un_unix(int(time.time()-tmp[3])))
				else: msg += L('Leave %s ago') % un_unix(int(time.time()-tmp[3]))					
				t7sp = tmp[7].split('\r')[0]
				if t7sp != '':
					if t7sp.count('\n') >= 4:
						stat = t7sp.split('\n',4)[4]
						if stat != '': msg += ' (%s)' % stat
					else: msg += ' (%s)' % t7sp
				if tmp[7].count('\r'): msg += ', %s %s' % (L('Client:'),' // '.join(tmp[7].split('\r')[-1].split(' // ')[:-1]))
			else: msg += L('Is here: %s') % un_unix(int(time.time()-tmp[3]))
			cnt += 1
			if not xtype: msg = msg.replace('\t',' - ')
	else: msg = L('Not found!')
	send_msg(type, jid, nick, msg)

def seen(type, jid, nick, text):
	seen_raw(type, jid, nick, text, None)
	
def seen_split(type, jid, nick, text):
	seen_raw(type, jid, nick, text, True)

def seen_raw(type, jid, nick, text, xtype):
	while text[-1:] == ' ': text = text[:-1]
	text = text.split('\n')
	llim = GT('age_default_limit')
	if len(text)>=2:
		try: llim = int(text[1])
		except: llim = GT('age_default_limit')
	text = text[0]
	if text == '': text = nick
	if llim > GT('age_max_limit'): llim = GT('age_max_limit')
	mdb = sqlite3.connect(agestatbase,timeout=base_timeout)
	cu = mdb.cursor()
	real_jid = cu.execute('select jid from age where room=? and (nick=? or jid=?) order by -status,-time',(jid,text,text.lower())).fetchone()
	if not real_jid:
		textt = '%'+text.lower()+'%'
		real_jid = cu.execute('select jid from age where room=? and (nick like ? or jid like ?) order by -status,-time',(jid,textt,textt)).fetchone()		
	if real_jid:
		if xtype: sbody = cu.execute('select * from age where room=? and jid=? order by -status,-time',(jid,real_jid[0])).fetchmany(llim)
		else: sbody = [cu.execute('select * from age where room=? and jid=? order by -status,-time',(jid,real_jid[0])).fetchone()]
	else: sbody = None
	if sbody:
		msg = L('I see:')
		cnt = 1
		for tmp in sbody:
			if xtype: msg += '\n%s. ' % cnt
			else: msg += ' '
			if text != tmp[1]: msg += L('%s (with nick: %s)') % (text,tmp[1])
			else: msg += tmp[1]
			if tmp[5]:
				if tmp[6] != '': msg += ' - '+ L('%s %s ago') % (tmp[6],un_unix(int(time.time()-tmp[3])))
				else: msg += ' - '+ L('Leave %s ago') % un_unix(int(time.time()-tmp[3]))
				t7sp = tmp[7].split('\r')[0]
				if t7sp != '':
					if t7sp.count('\n') >= 4:
						stat = t7sp.split('\n',4)[4]
						if stat != '': msg += ' (%s)' % stat
					else: msg += ' (%s)' % t7sp
				if tmp[7].count('\r'): msg += ', %s %s' % (L('Client:'),' // '.join(tmp[7].split('\r')[-1].split(' // ')[:-1]))
			else: msg += ' - '+ L('Is here: %s') % un_unix(int(time.time()-tmp[3]))
			cnt += 1
	else: msg = L('Not found!')
	send_msg(type, jid, nick, msg)

def seenjid(type, jid, nick, text):
	seenjid_raw(type, jid, nick, text, None)
	
def seenjid_split(type, jid, nick, text):
	seenjid_raw(type, jid, nick, text, True)
	
def seenjid_raw(type, jid, nick, text, xtype):
	while text[-1:] == ' ': text = text[:-1]
	text = text.split('\n')
	llim = GT('age_default_limit')
	if len(text)>=2:
		try: llim = int(text[1])
		except: llim = GT('age_default_limit')
	text = text[0]
	ztype = None
	if text == '': text = nick
	if llim > GT('age_max_limit'): llim = GT('age_max_limit')
	mdb = sqlite3.connect(agestatbase,timeout=base_timeout)
	cu = mdb.cursor()
	real_jid = cu.execute('select jid from age where room=? and (nick=? or jid=?) group by jid order by -status,-time',(jid,text,text.lower())).fetchall()
	if not real_jid:
		txt = '%'+text.lower()+'%'
		real_jid = cu.execute('select jid from age where room=? and (nick like ? or jid like ?) group by jid order by -status,-time',(jid,txt,txt)).fetchall()		
	if real_jid:
		sbody = []
		for rj in real_jid:
			if xtype: sb = cu.execute('select * from age where room=? and jid=? order by status, jid',(jid,rj[0])).fetchall()
			else: sb = cu.execute('select room, nick, jid, time, sum(age), status, type, message from age where room=? and jid=? order by status, jid',(jid,rj[0])).fetchall()
			for tmp in sb: sbody.append(tmp)
		sbody = sbody[:llim]
	else: sbody = None
	if sbody:
		ztype = True
		msg = L('I saw %s:') % text
		cnt = 1
		for tmp in sbody:
			msg += '\n'+str(cnt)+'. ' + tmp[1] + ' ('+tmp[2]+')'
			if tmp[5]:
				if tmp[6] != '': msg += '\t'+ L('%s %s ago') % (tmp[6],un_unix(int(time.time()-tmp[3])))
				else: msg += '\t'+ L('Leave %s ago') % un_unix(int(time.time()-tmp[3]))					
				t7sp = tmp[7].split('\r')[0]
				if t7sp != '':
					if t7sp.count('\n') >= 4:
						stat = t7sp.split('\n',4)[4]
						if stat != '': msg += ' (%s)' % stat
					else: msg += ' (%s)' % t7sp
				if tmp[7].count('\r'): msg += ', %s %s' % (L('Client:'),tmp[7].split('\r')[-1])
			else: msg += '\t'+ L('Is here: %s') % un_unix(int(time.time()-tmp[3]))
			cnt += 1
			if not xtype: msg = msg.replace('\t',' - ')
	else: msg = L('Not found!')
	if type == 'groupchat' and ztype:
		send_msg(type,jid,nick,L('Send for you in private'))
		send_msg('chat', jid, nick, msg)
	else: send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'age', true_age, 2, L('Show age of jid in conference.')),
	 (3, 'age_split', true_age_split, 2, L('Show age of jid in conference splitted by nicks.')),
	 (3, 'seen', seen, 2, L('Show time of join/leave.')),
	 (3, 'seen_split', seen_split, 2, L('Show time of join/leave splitted by nicks.')),
	 (7, 'seenjid', seenjid, 2, L('Show time of join/leave + jid.')),
	 (7, 'seenjid_split', seenjid_split, 2, L('Show time of join/leave + jid splitted by nicks.'))]
