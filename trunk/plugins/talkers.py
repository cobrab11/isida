#!/usr/bin/python
# -*- coding: utf-8 -*-

def gtalkers(type, jid, nick, text):
	mdb = sqlite3.connect(talkersbase)
	cu = mdb.cursor()
	if len(text):
		ttext = '%'+text+'%'
		tma = cu.execute('select * from talkers where (jid like ? or nick like ? or room like ?) order by -words',(ttext,ttext,ttext)).fetchmany(10)
	else: tma = cu.execute('select * from talkers order by -words').fetchmany(10)
	if len(tma):
		msg = L('Talkers:\nNick\t\tWords\tPhrases\tEffect\tConference')
		cnd = 1
		for tt in tma:
			msg += '\n'+str(cnd)+'. '+tt[2] +'\t\t'+ str(tt[3]) +'\t'+ str(tt[4]) + '\t'+ str(float(int(float(tt[3])/float(tt[4])*100))/100) + '\t' + getName(tt[0])
			cnd += 1
	else: msg = text +' '+L('Not found!')
	send_msg(type, jid, nick, msg)

def talkers(type, jid, nick, text):
	mdb = sqlite3.connect(talkersbase)
	cu = mdb.cursor()
	if len(text):
		ttext = '%'+text+'%'
		tma = cu.execute('select * from talkers where room=? and (jid like ? or nick like ?) order by -words',(jid,ttext,ttext)).fetchmany(10)
	else: tma = cu.execute('select * from talkers where room=? order by -words',(jid,)).fetchmany(10)
	if len(tma):
		msg = L('Talkers:\nNick\t\tWords\tPhrases\tEffect')
		cnd = 1
		for tt in tma:
			msg += '\n'+str(cnd)+'. '+tt[2] +'\t\t'+ str(tt[3]) +'\t'+ str(tt[4]) + '\t'+ str(float(int(float(tt[3])/float(tt[4])*100))/100)
			cnd += 1
	else: msg = text +' '+L('Not found!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'talkers', talkers, 2, L('Show local talkers')),
	   (4, 'gtalkers', gtalkers, 2, L('Show global talkers'))]
