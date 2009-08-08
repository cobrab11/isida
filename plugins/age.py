#!/usr/bin/python
# -*- coding: utf -*-

def true_age(type, jid, nick, text):
	while text[-1:] == ' ': text = text[:-1]
	text = text.split(' ')
	llim = 10
	if len(text)>=2:
		try: llim = int(text[0])
		except: llim = 10
		text = text[1]
	else: text = text[0]
	if text != '':
		if llim > 100: llim = 100
		is_found = 0
		ms = []
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		text = '%'+text.lower()+'%'
		sbody = cu.execute('select * from age where room=? and (nick like ? or jid like ?) order by -time,-status',(jid,text,text)).fetchmany(llim)
		if sbody:
			msg = u'Я видела:'
			cnt = 1
			for tmp in sbody:
				if tmp[5]: r_age = tmp[4]
				else: r_age = int(time.time())-tmp[3]+tmp[4]
				msg += '\n'+str(cnt)+'. '+tmp[1]+u'\t'+un_unix(r_age)+u', '

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
		else: msg = u'Не найдено!'
	else: msg = u'Ась?'
	send_msg(type, jid, nick, msg)

def seen(type, jid, nick, text):
	while text[-1:] == ' ': text = text[:-1]
	text = text.split(' ')
	llim = 10
	if len(text)>=2:
		try: llim = int(text[0])
		except: llim = 10
		text = text[1]
	else: text = text[0]
	if text != '':
		if llim > 100: llim = 100
		is_found = 0
		ms = []
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		text = '%'+text.lower()+'%'
		sbody = cu.execute('select * from age where room=? and (nick like ? or jid like ?) order by -time,-status',(jid,text,text)).fetchmany(llim)
		if sbody:
			msg = u'Я видела:'
			cnt = 1
			for tmp in sbody:
				msg += '\n'+str(cnt)+'. '+tmp[1]

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
		else: msg = u'Не найдено!'
	else: msg = u'Ась?'
	send_msg(type, jid, nick, msg)

def seenjid(type, jid, nick, text):
	while text[-1:] == ' ': text = text[:-1]
	text = text.split(' ')
	llim = 10
	if len(text)>=2:
		try: llim = int(text[0])
		except: llim = 10
		text = text[1]
	else: text = text[0]
	xtype = None
	if text != '':
		if llim > 100: llim = 100
		is_found = 0
		ms = []
		mdb = sqlite3.connect(agestatbase)
		cu = mdb.cursor()
		text = '%'+text.lower()+'%'
		sbody = cu.execute('select * from age where room=? and (nick like ? or jid like ?) order by -time,-status',(jid,text,text)).fetchmany(llim)
		if sbody:
			xtype = True
			msg = u'Я видела:'
			cnt = 1
			for tmp in sbody:
				msg += '\n'+str(cnt)+'. '+tmp[1]+' ('+tmp[2]+')'

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
		else: msg = u'Не найдено!'
	else: msg = u'Ась?'

	if type == 'groupchat' and xtype:
		send_msg(type,jid,nick,u'Результат отправлен Вам в приват.')
		send_msg('chat', jid, nick, msg)
	else:
		send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'age', true_age, 2, u'Показывает какое время определённый jid или ник находился в данной конференции.\nage [number][word]\nnumber - максимальное количество при поиске,\nword - поиск слова в нике/jid\'е'),
	 (0, u'seen', seen, 2, u'Показывает время входа/выхода.'),
	 (1, u'seenjid', seenjid, 2, u'Показывает время входа/выхода + jid. Результат работы команды всегда направляется в приват.')]
