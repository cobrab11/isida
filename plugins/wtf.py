#!/usr/bin/python
# -*- coding: utf -*-

def wtfsearch(type, jid, nick, text):
	msg = u'Чего искать то будем?'
	if len(text):
		mdb = sqlite3.connect(wtfbase)
		cu = mdb.cursor()
		text = '%'+text+'%'
		ww = cu.execute('select * from wtf where (room=? or room=? or room=?) and (room like ? or jid like ? or nick like ? or wtfword like ? or wtftext like ? or time like ?)',(jid,'global','import',text,text,text,text,text,text)).fetchall()
		msg = ''
		for www in ww:
			msg += www[4]+', '

		if len(msg):
			msg = u'Нечто похожее я видела в: '+msg[:-2]
		else:
			msg = u'Хм. Ничего похожего я не знаю...'

	send_msg(type, jid, nick, msg)

def wtfrand(type, jid, nick):
	msg = u'Всё, что я знаю это: '
	mdb = sqlite3.connect(wtfbase)
	cu = mdb.cursor()
	ww = cu.execute('select * from wtf where room=? or room=? or room=?',(jid,'global','import')).fetchall()
	tlen = len(ww)
	ww = ww[randint(0,tlen-1)]
	msg = u'Я знаю, что '+ww[4]+u' - '+ww[5]
	send_msg(type, jid, nick, msg)

def wtfnames(type, jid, nick, text):
	msg = u'Всё, что я знаю это: '
	mdb = sqlite3.connect(wtfbase)
	cu = mdb.cursor()
	if text == 'all': cu.execute('select * from wtf where room=? or room=? or room=?',(jid,'global','import'))
	elif text == 'global': cu.execute('select * from wtf where room=?',('global',))
	elif text == 'import': cu.execute('select * from wtf where room=?',('import',))
	else: cu.execute('select * from wtf where room=?',(jid,))
	for ww in cu: msg += ww[4]+', '
	msg=msg[:-2]
	send_msg(type, jid, nick, msg)

def wtfcount(type, jid, nick):
	mdb = sqlite3.connect(wtfbase)
	cu = mdb.cursor()
	tlen = len(cu.execute('select * from wtf where 1=1').fetchall())
	cnt = len(cu.execute('select * from wtf where room=?',(jid,)).fetchall())
	glb = len(cu.execute('select * from wtf where room=?',('global',)).fetchall())
	imp = len(cu.execute('select * from wtf where room=?',('import',)).fetchall())
	msg = u'В этой конфе определений: '+str(cnt)+u'\nГлобальных: '+str(glb)+u'\nИмпортировано: '+str(imp)+u'\nВсего: '+str(tlen)
	send_msg(type, jid, nick, msg)
	mdb.close()

def wtf(type, jid, nick, text):
	wtf_get(0,type, jid, nick, text)

def wtff(type, jid, nick, text):
	wtf_get(1,type, jid, nick, text)

def wwtf(type, jid, nick, text):
	wtf_get(2,type, jid, nick, text)

def wtfp(type, jid, nick, text):
	if text.count('\n'):
		text = text.split('\n')
		tnick = text[1]
		ttext = text[0]
		is_found = 0
		for mmb in megabase:
			if mmb[0]==jid and mmb[1]==tnick:
				is_found = 1
				break
		if is_found:
			wtf_get(0,'chat', jid, tnick, ttext)
			send_msg(type, jid, nick, u'Отправлено в приват '+tnick)
		else: send_msg(type, jid, nick, u'Ник '+tnick+u' не найден!')
	else: wtf_get(0,'chat', jid, nick, text)

def wtf_get(ff,type, jid, nick, text):
	msg = u'Чего искать то будем?'
	if len(text):
		mdb = sqlite3.connect(wtfbase)
		cu = mdb.cursor()
		tlen = len(cu.execute('select * from wtf where (room=? or room=? or room=?) and wtfword=?',(jid,'global','import',text)).fetchall())
		cu.execute('select * from wtf where (room=? or room=? or room=?) and wtfword=?',(jid,'global','import',text))

		if tlen:
			for aa in cu: ww=aa[1:]
			msg = u'Я знаю, что '+text+u' - '+ww[4]
			if ff == 1: msg += u'\nот: '+ww[2]+' ['+ww[5]+']'
			elif ff == 2: msg = u'Я знаю, что '+text+u' было определено: '+ww[2]+' ('+ww[1]+')'+' ['+ww[5]+']'
		else: msg = u'Хм. Мне про это никто не рассказывал...'
	send_msg(type, jid, nick, msg)

def dfn(type, jid, nick, text):
	global wbase, wtfbase
	msg = u'Чего запомнить то надо?'
	if len(text) and text.count('='):

		ta = get_access(jid,nick)

		realjid =ta[1]

		ti = text.index('=')
		what = del_space_end(text[:ti])
		text = del_space_begin(text[ti+1:])

		mdb = sqlite3.connect(wtfbase)
		cu = mdb.cursor()
		tlen = len(cu.execute('select * from wtf where (room=? or room=? or room=?) and wtfword=?',(jid,'global','import',what)).fetchall())
		cu.execute('select * from wtf where (room=? or room=? or room=?) and wtfword=?',(jid,'global','import',what))
		
		if tlen:
			for aa in cu: ww=aa
			if ww[1] == 'global':
				msg = u'Это глобальное определение и его нельзя изменить!'
				text = ''
			else:
				if text == '': msg = u'Жаль, что такую полезную хренотень надо забыть...'
				else: msg = u'Боян, но я запомню!'
				cu.execute('delete from wtf where wtfword=?',(what,))
			idx = ww[0]
		else:
			msg = u'Ммм.. Что-то новенькое, ща запомню!'
			idx = len(cu.execute('select * from wtf where 1=1').fetchall())

		if text != '': cu.execute('insert into wtf values (?,?,?,?,?,?,?)', (idx, jid, realjid, nick, what, text, timeadd(tuple(localtime()))))
		mdb.commit()
	send_msg(type, jid, nick, msg)

def gdfn(type, jid, nick, text):
	global wbase, wtfbase
	msg = u'Чего запомнить то надо?'
	if len(text) and text.count('='):

		ta = get_access(jid,nick)

		realjid =ta[1]

		ti = text.index('=')
		what = del_space_end(text[:ti])
		text = del_space_begin(text[ti+1:])

		mdb = sqlite3.connect(wtfbase)
		cu = mdb.cursor()
		tlen = len(cu.execute('select * from wtf where (room=? or room=? or room=?) and wtfword=?',(jid,'global','import',what)).fetchall())
		cu.execute('select * from wtf where (room=? or room=? or room=?) and wtfword=?',(jid,'global','import',what))
		
		if tlen:
			for aa in cu: ww=aa
			if text == '': msg = u'Жаль, что такую полезную хренотень надо забыть...'
			else: msg = u'Боян, но я запомню!'
			cu.execute('delete from wtf where wtfword=?',(what,))
			idx = ww[0]
		else:
			msg = u'Ммм.. Что-то новенькое, ща запомню!'
			idx = len(cu.execute('select * from wtf where 1=1').fetchall())

		if text != '': cu.execute('insert into wtf values (?,?,?,?,?,?,?)', (idx, 'global', realjid, nick, what, text, timeadd(tuple(localtime()))))
		mdb.commit()
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'wtfrand', wtfrand, 1, u'Показ случайного обределения из базы слов.'),
	 (0, u'wtfnames', wtfnames, 2, u'Показ списка определений в конференции.\nwtfnames [all|global|import]'),
	 (0, u'wtfcount', wtfcount, 1, u'Показ количества определений в конференции.'),
	 (0, u'wtfsearch', wtfsearch, 2, u'Поиск по базе определний.'),
	 (2, u'wwtf', wwtf, 2, u'Показ инфонмации о том, кто сделал определение.'),
	 (0, u'wtff', wtff, 2, u'Показ определения вместе с ником и датой.'),
	 (0, u'wtfp', wtfp, 2, u'Показ определения в приват, независимо от куда поступила команда.\nwtfp word - показать определение word себе в приват\nwtfp word\nnick - показать определение word в приват nick'),
	 (0, u'wtf', wtf, 2, u'Показ определения.'),
	 (1, u'dfn', dfn, 2, u'Установка определения.\ndfn word=definition - запоминает definition как определение word\ndfn word= - удаляет определение word'),
	 (2, u'gdfn', gdfn, 2, u'Установка глобального определения.\ngdfn word=definition - запоминает definition как определение word\ngdfn word= - удаляет определение word')]
