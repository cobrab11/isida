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
		except: llim = 10
	text = text[0]
	if text == '': text = nick
	if llim > 100: llim = 100
	mdb = sqlite3.connect(agestatbase)
	cu = mdb.cursor()
	real_jid = cu.execute('select jid from age where room=? and (nick=? or jid=?) order by -time,-status',(jid,text,text.lower())).fetchone()
	if not real_jid:
		text = '%'+text.lower()+'%'
		real_jid = cu.execute('select jid from age where room=? and (nick like ? or jid like ?) order by -time,-status',(jid,text,text)).fetchone()		
	try:
		if xtype: sbody = cu.execute('select * from age where room=? and jid=? order by status',(jid,real_jid[0])).fetchmany(llim)
		else: sbody = cu.execute('select room, nick, jid, time, sum(age), status, type, message from age where room=? and jid=? order by status',(jid,real_jid[0])).fetchmany(llim)
	except: sbody = None
	if sbody:
		msg = u'Я видела:'
		cnt = 1
		for tmp in sbody:
			if tmp[5]: r_age = tmp[4]
			else: r_age = int(time.time())-tmp[3]+tmp[4]
			if xtype: msg += '\n'+str(cnt)+'. '+tmp[1]
			else: msg += ' '+tmp[1]
			msg += u'\t'+un_unix(r_age)+u', '

			if tmp[5]:
				if tmp[6] != '': msg += tmp[6]+' '+un_unix(int(time.time()-tmp[3]))+u' назад'
				else: msg += u'Вышел '+un_unix(int(time.time()-tmp[3]))+u' назад'
				if tmp[7] != '':
					if tmp[7].count('\n') >= 4:
						stat = tmp[7].split('\n',4)[4]
						if stat != '': msg += ' ('+stat+')'
					else: msg += ' ('+tmp[7]+')'
			else: msg += u'находится тут: '+un_unix(int(time.time()-tmp[3]))
			cnt += 1
			if not xtype: msg = msg.replace('\t',' - ')
	else: msg = u'Не найдено!'
	send_msg(type, jid, nick, msg)

def seen(type, jid, nick, text):
	seen_raw(type, jid, nick, text, None)
	
def seen_split(type, jid, nick, text):
	seen_raw(type, jid, nick, text, True)

def seen_raw(type, jid, nick, text, xtype):
	while text[-1:] == ' ': text = text[:-1]
	text = text.split('\n')
	llim = 10
	if len(text)>=2:
		try: llim = int(text[1])
		except: llim = 10
	text = text[0]
	if text == '': text = nick
	if llim > 100: llim = 100
	mdb = sqlite3.connect(agestatbase)
	cu = mdb.cursor()
	real_jid = cu.execute('select jid from age where room=? and (nick=? or jid=?) order by -time,-status',(jid,text,text.lower())).fetchone()
	if not real_jid:
		textt = '%'+text.lower()+'%'
		real_jid = cu.execute('select jid from age where room=? and (nick like ? or jid like ?) order by -time,-status',(jid,textt,textt)).fetchone()		
	if real_jid:
		if xtype: sbody = cu.execute('select * from age where room=? and jid=? order by status',(jid,real_jid[0])).fetchmany(llim)
		else: sbody = cu.execute('select room, nick, jid, time, sum(age), status, type, message from age where room=? and jid=? order by status',(jid,real_jid[0])).fetchmany(llim)
	else: sbody = None
	if sbody:
		msg = u'Я видела:'
		cnt = 1
		for tmp in sbody:
			if xtype: msg += '\n'+str(cnt)+'. '
			else: msg += ' '
			if text != tmp[1]: msg += text+u' (с ником: '+tmp[1]+')'
			else: msg += tmp[1] 
			if tmp[5]:
				if tmp[6] != '': msg += u'\t'+tmp[6]+' '+un_unix(int(time.time()-tmp[3]))+u' назад'
				else: msg += u'\tВышел '+un_unix(int(time.time()-tmp[3]))+u' назад'
				if tmp[7] != '':
					if tmp[7].count('\n') >= 4:
						stat = tmp[7].split('\n',4)[4]
						if stat != '': msg += ' ('+stat+')'
					else: msg += ' ('+tmp[7]+')'
			else: msg += u'\tнаходится тут: '+un_unix(int(time.time()-tmp[3]))
			cnt += 1
			if not xtype: msg = msg.replace('\t',' - ')
	else: msg = u'Не найдено!'
	send_msg(type, jid, nick, msg)

def seenjid(type, jid, nick, text):
	seenjid_raw(type, jid, nick, text, None)
	
def seenjid_split(type, jid, nick, text):
	seenjid_raw(type, jid, nick, text, True)
	
def seenjid_raw(type, jid, nick, text, xtype):
	while text[-1:] == ' ': text = text[:-1]
	text = text.split('\n')
	llim = 10
	if len(text)>=2:
		try: llim = int(text[1])
		except: llim = 10
	text = text[0]
	ztype = None
	if text == '': text = nick
	if llim > 100: llim = 100
	mdb = sqlite3.connect(agestatbase)
	cu = mdb.cursor()
	real_jid = cu.execute('select jid from age where room=? and (nick=? or jid=?) group by jid order by -time,-status',(jid,text,text.lower())).fetchall()
	if not real_jid:
		txt = '%'+text.lower()+'%'
		real_jid = cu.execute('select jid from age where room=? and (nick like ? or jid like ?) group by jid order by -time,-status',(jid,txt,txt)).fetchall()		
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
		msg = u'Я видела '+text+u':'
		cnt = 1
		for tmp in sbody:
			msg += '\n'+str(cnt)+'. ' + tmp[1] + ' ('+tmp[2]+')'
			if tmp[5]:
				if tmp[6] != '': msg += u'\t'+tmp[6]+' '+un_unix(int(time.time()-tmp[3]))+u' назад'
				else: msg += u'\tВышел '+un_unix(int(time.time()-tmp[3]))+u' назад'
				if tmp[7] != '':
					if tmp[7].count('\n') >= 4:
						stat = tmp[7].split('\n',4)[4]
						if stat != '': msg += ' ('+stat+')'
					else: msg += ' ('+tmp[7]+')'
			else: msg += u'\tнаходится тут: '+un_unix(int(time.time()-tmp[3]))
			cnt += 1
			if not xtype: msg = msg.replace('\t',' - ')
	else: msg = u'Не найдено!'
	if type == 'groupchat' and ztype:
		send_msg(type,jid,nick,u'Результат отправлен Вам в приват.')
		send_msg('chat', jid, nick, msg)
	else: send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'age', true_age, 2, u'Показывает какое время определённый jid или ник находился в данной конференции.'),
	 (0, u'age_split', true_age_split, 2, u'Показывает какое время определённый jid или ник находился в данной конференции с разбивкой по никам.'),
	 (0, u'seen', seen, 2, u'Показывает время входа/выхода.'),
	 (0, u'seen_split', seen_split, 2, u'Показывает время входа/выхода с разбивкой по никам.'),
	 (1, u'seenjid', seenjid, 2, u'Показывает время входа/выхода + jid. Результат работы команды всегда направляется в приват.'),
	 (1, u'seenjid_split', seenjid_split, 2, u'Показывает время входа/выхода + jid с разбивкой по никам. Результат работы команды всегда направляется в приват.')]
