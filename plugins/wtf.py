#!/usr/bin/python
# -*- coding: utf -*-

def wtfsearch(type, jid, nick, text):
	msg = L('What need to find?')
	if len(text):
		mdb = sqlite3.connect(wtfbase)
		cu = mdb.cursor()
		text = '%'+text+'%'
		ww = cu.execute('select * from wtf where (room=? or room=? or room=?) and (room like ? or jid like ? or nick like ? or wtfword like ? or wtftext like ? or time like ?)',(jid,'global','import',text,text,text,text,text,text)).fetchall()
		msg = ''
		for www in ww: msg += www[4]+', '
		if len(msg): msg = L('Some matches in definitions: %s') % msg[:-2]
		else: msg = L('No matches.')
	send_msg(type, jid, nick, msg)

def wtfrand(type, jid, nick):
	mdb = sqlite3.connect(wtfbase)
	cu = mdb.cursor()
	ww = cu.execute('select * from wtf where room=? or room=? or room=?',(jid,'global','import')).fetchall()
	tlen = len(ww)
	ww = ww[randint(0,tlen-1)]
	msg = L('I know that %s is %s') % (ww[4],ww[5])
	send_msg(type, jid, nick, msg)

def wtfnames(type, jid, nick, text):
	mdb = sqlite3.connect(wtfbase)
	cu = mdb.cursor()
	if text == 'all': cu.execute('select * from wtf where room=? or room=? or room=?',(jid,'global','import'))
	elif text == 'global': cu.execute('select * from wtf where room=?',('global',))
	elif text == 'import': cu.execute('select * from wtf where room=?',('import',))
	else: cu.execute('select * from wtf where room=?',(jid,))
	msg = ''
	for ww in cu: msg += ww[4]+', '
	if len(msg): msg = L('All I know is: %s') % msg[:-2]
	else: msg = L('No matches.')
	send_msg(type, jid, nick, msg)

def wtfcount(type, jid, nick):
	mdb = sqlite3.connect(wtfbase)
	cu = mdb.cursor()
	tlen = len(cu.execute('select * from wtf where 1=1').fetchall())
	cnt = len(cu.execute('select * from wtf where room=?',(jid,)).fetchall())
	glb = len(cu.execute('select * from wtf where room=?',('global',)).fetchall())
	imp = len(cu.execute('select * from wtf where room=?',('import',)).fetchall())
	msg = L('Locale definition: %s\nGlobal: %s\nImported: %s\nTotal: %s') % (str(cnt),str(glb),str(imp),str(tlen))
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
			send_msg(type, jid, nick, L('Send to private %s') % tnick)
		else: send_msg(type, jid, nick, L('Nick %s not found!') % tnick)
	else: wtf_get(0,'chat', jid, nick, text)

def wtf_get(ff,type, jid, nick, text):
	if len(text):
		mdb = sqlite3.connect(wtfbase)
		cu = mdb.cursor()
		tlen = len(cu.execute('select * from wtf where (room=? or room=? or room=?) and wtfword=?',(jid,'global','import',text)).fetchall())
		cu.execute('select * from wtf where (room=? or room=? or room=?) and wtfword=?',(jid,'global','import',text))

		if tlen:
			for aa in cu: ww=aa[1:]
			msg = L('I know that %s is %s') % (text,ww[4])
			if ff == 1: msg += L('\nfrom: %s %s') % (ww[2],'['+ww[5]+']')
			elif ff == 2: msg = L('I know that %s was defined by %s %s %s') % (text,ww[2],'('+ww[1]+')','['+ww[5]+']')
		else: msg = L('I don\'t know!')
	else: msg = L('What search?')
	send_msg(type, jid, nick, msg)

def dfn(type, jid, nick, text):
	global wbase, wtfbase
	if len(text) and text.count('='):
		ta = get_level(jid,nick)
		realjid =ta[1]
		al = ta[0]

		ti = text.index('=')
		what = del_space_end(text[:ti])
		text = del_space_begin(text[ti+1:])

		mdb = sqlite3.connect(wtfbase)
		cu = mdb.cursor()
		matches = cu.execute('select * from wtf where (room=? or room=? or room=?) and wtfword=? order by lim',(jid,'global','import',what)).fetchone()
		if matches:
			if matches[7] > al:
				msg,text = L('Not enough rights!'),''
				try: msg += ' ' + unlevltxt[unlevlnum[matches[7]]] % unlevl[matches[7]]
				except: pass
			elif matches[1] == 'global': msg, text = L('This is global definition and not allowed to change!'), ''
			elif text == '':
				msg = L('Definition removed!')
				cu.execute('delete from wtf where wtfword=? and room=?',(what,jid))
			else:
				msg = L('Definition updated!')
				cu.execute('delete from wtf where wtfword=? and room=?',(what,jid))
		elif text == '': msg = L('Nothing to remove!')
		else: msg = L('Definition saved!')
		idx = len(cu.execute('select * from wtf where 1=1').fetchall())
		if text != '': cu.execute('insert into wtf values (?,?,?,?,?,?,?,?)', (idx, jid, realjid, nick, what, text, timeadd(tuple(localtime())),al))
		mdb.commit()
	else: msg = L('What need to remember?')
	send_msg(type, jid, nick, msg)

def gdfn(type, jid, nick, text):
	global wbase, wtfbase
	if len(text) and text.count('='):
		ta = get_level(jid,nick)
		realjid =ta[1]
		al = ta[0]

		ti = text.index('=')
		what = del_space_end(text[:ti])
		text = del_space_begin(text[ti+1:])

		mdb = sqlite3.connect(wtfbase)
		cu = mdb.cursor()
		matches = cu.execute('select * from wtf where (room=? or room=? or room=?) and wtfword=? order by lim',(jid,'global','import',what)).fetchone()
		if matches:
			if matches[7] > al: 
				msg,text = L('Not enough rights!'),''
				try: msg += ' ' + unlevltxt[unlevlnum[matches[7]]] % unlevl[matches[7]]
				except: pass
			elif text == '':
				msg = L('Definition removed!')
				cu.execute('delete from wtf where wtfword=?',(what,))
			else:
				msg = L('Definition updated!')
				cu.execute('delete from wtf where wtfword=?',(what,))
		elif text == '': msg = L('Nothing to remove!')
		else: msg = L('Definition saved!')
		idx = len(cu.execute('select * from wtf where 1=1').fetchall())
		if text != '': cu.execute('insert into wtf values (?,?,?,?,?,?,?,?)', (idx, 'global', realjid, nick, what, text, timeadd(tuple(localtime())),al))
		mdb.commit()
	else: msg = L('What need to remember?')
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, 'wtfrand', wtfrand, 1, L('Random definition from base.')),
	 (0, 'wtfnames', wtfnames, 2, L('List of definitions in conference.\nwtfnames [all|global|import]')),
	 (0, 'wtfcount', wtfcount, 1, L('Definitions count.')),
	 (0, 'wtfsearch', wtfsearch, 2, L('Search in definitions base.')),
	 (2, 'wwtf', wwtf, 2, L('Information about definition commiter.')),
	 (0, 'wtff', wtff, 2, L('Show definition with nick and date.')),
	 (0, 'wtfp', wtfp, 2, L('Show definition in private.\nwtfp word\n[nick]')),
	 (0, 'wtf', wtf, 2, L('Show definition.')),
	 (0, 'dfn', dfn, 2, L('Set definition.\ndfn word=definition - remember definition as word\ndfn word= - remove definition word')),
	 (0, 'gdfn', gdfn, 2, L('Set global definition.\ngdfn word=definition - remember definition as word\ngdfn word= - remove definition word'))]
