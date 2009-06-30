#!/usr/bin/python
# -*- coding: utf -*-

# Поиск по глобальной базе "болтунов"
def gtalkers(type, jid, nick, text):
	mdb = sqlite3.connect(mainbase)
	cu = mdb.cursor()
	if len(text):
		ttext = '%'+text+'%'
		tma = cu.execute('select * from talkers where (jid like ? or nick like ? or room like ?) order by -words',(ttext,ttext,ttext)).fetchmany(10)
	else:
		tma = cu.execute('select * from talkers order by -words').fetchmany(10)

        wtext = text.split(' ')
        wtext = len(wtext)
        beadd = 1

	if len(tma):
	        msg = u'Болтуны:\nНик\t\tСлов\tФраз\tКоэф.\tКонфа'
		cnd = 1
		for tt in tma:
        	        msg += u'\n'+str(cnd)+'. '+tt[2] +'\t\t'+ str(tt[3]) +u'\t'+ str(tt[4]) + u'\t'+ str(float(int(float(tt[3])/float(tt[4])*100))/100) + u'\t' + getName(tt[0])
			cnd += 1
	else:
		msg = text +u' не найдено!'
	send_msg(type, jid, nick, msg)
	

# Поиск по базе "блтунов" в пределах одной конференции
def talkers(type, jid, nick, text):
	mdb = sqlite3.connect(mainbase)
	cu = mdb.cursor()
	if len(text):
		ttext = '%'+text+'%'
		tma = cu.execute('select * from talkers where room=? and (jid like ? or nick like ?) order by -words',(jid,ttext,ttext)).fetchmany(10)
	else:
		tma = cu.execute('select * from talkers where room=? order by -words',(jid,)).fetchmany(10)

        wtext = text.split(' ')
        wtext = len(wtext)
        beadd = 1

	if len(tma):
	        msg = u'Болтуны:\nНик\t\tСлов\tФраз\tКоэф.'
		cnd = 1
		for tt in tma:
        	        msg += u'\n'+str(cnd)+'. '+tt[2] +'\t\t'+ str(tt[3]) +u'\t'+ str(tt[4]) + u'\t'+ str(float(int(float(tt[3])/float(tt[4])*100))/100)
			cnd += 1
	else:
		msg = text +u' не найдено!'
	send_msg(type, jid, nick, msg)

#------------------------------------------------

# в начале
# 0 - всем
# 1 - админам\овнерам
# 2 - владельцу бота

# в конце
# 0 - передавать параметры
# 1 - ничего не передавать
# 2 - передавать остаток текста

global execute, timer

timer = []

execute = [(1, u'talkers', talkers, 2),
	   (1, u'gtalkers', gtalkers, 2)]
