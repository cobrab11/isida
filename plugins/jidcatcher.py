#!/usr/bin/python
# -*- coding: utf -*-

jid_base = set_folder+u'jidbase.db'		# статистика jid'ов

def info_search(type, jid, nick, text):
	msg = u'Чего искать то будем?'
	if text != '':
		mdb = sqlite3.connect(jid_base)
		cu = mdb.cursor()
		cu.execute('delete from jid where server like ?',('<temporary>%',)).fetchall()
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

def info_res(type, jid, nick, text):
	mdb = sqlite3.connect(jid_base)
	cu = mdb.cursor()
	cu.execute('delete from jid where server like ?',('<temporary>%',)).fetchall()
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
	cu.execute('delete from jid where server like ?',('<temporary>%',)).fetchall()
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

def jidcatcher_presence(room,jid,nick,type,text):
	if jid != 'None':
		mdb = sqlite3.connect(jid_base)
		cu = mdb.cursor()
		aa1 = getName(jid)
		aa2 = getServer(jid)
		aa3 = getResourse(jid)
		if aa2[:11] != '<temporary>':
			try:
				if not cu.execute('select * from jid where login=? and server=? and resourse=?',(aa1,aa2,aa3)).fetchall():
					cu.execute('insert into jid values (?,?,?)', (aa1,aa2,aa3))
					mdb.commit()
			except: pass

global execute, presence_control

presence_control = [jidcatcher_presence]

execute = [(1, u'res', info_res, 2, u'Без параметра показывает топ10 рессурсов по всем конференциям, где находится бот.\nС параметром - поиск по базе рессурсов.\nЧисла - количество рессурсов.'),
		   (1, u'serv', info_serv, 2, u'Без параметра показывает все сервера, с которых заходили в конференции, где находится бот.\nС параметром - поиск по базе серверов.\nЕсли параметр count - показывает количество уникальных серверов.\nЧисла - количество серверов.'),
		   (2, u'search', info_search, 2, u'Поиск по внутренней базе jid\'ов.'),]
