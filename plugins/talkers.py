#!/usr/bin/python
# -*- coding: utf -*-

tab_size = 12

# Поиск по глобальной базе "болтунов"
def gtalkers(type, jid, nick, text):
	tbasefile = 'settings/talkers'
        if os.path.isfile(tbasefile):
        	tbase = eval(readfile(tbasefile))
        else:
        	tbase = []
        	writefile(tbasefile,str(tbase))
        jidc = []
        
        if text == '':
                for tt in tbase:
                        jidc.append(tt)
        else:
                for tt in tbase:
                        if tt[2].lower().count(text.lower())+tt[1].lower().count(text.lower()):
                                jidc.append(tt)                                

	for i in range(0,len(jidc)):
		for j in range(i,len(jidc)):
			if jidc[i][3] < jidc[j][3]:
				jj = jidc[i]
				jidc[i] = jidc[j]
				jidc[j] = jj

        if len(jidc)> 10:
                jidc = jidc[:10]
	maxlen = 0
	for tt in jidc:
		if len(tt[2])>maxlen:
			maxlen=len(tt[2])
	tabz = ''
	while maxlen >=0:
		tabz+='\t'
		maxlen -= tab_size

        msg = u'Болтуны:\nНик'+tabz+u'Слов\tФраз\tКоэф.\tКонфа'

        for tt in jidc:
		ml = len(tt[2])
		ttz = tabz
		while ml >= tab_size:
			ttz = ttz[:-1]
			ml -= tab_size
                msg += u'\n'+tt[2] +ttz+ str(tt[3]) +u'\t'+ str(tt[4]) + u'\t'+ str(float(int(float(tt[3])/float(tt[4])*100))/100) + u'\t' + getName(tt[0])
	send_msg(type, jid, nick, msg)
	

# Поиск по базе "блтунов" в пределах одной конференции
def talkers(type, jid, nick, text):
	tbasefile = 'settings/talkers'
        if os.path.isfile(tbasefile):
        	tbase = eval(readfile(tbasefile))
        else:
        	tbase = []
        	writefile(tbasefile,str(tbase))
        jidc = []
        msg = u'Болтуны:\nНик\tСлов\tФраз\tКоэф.'
        
        if text == '':
                for tt in tbase:
                        if jid == tt[0]:
                                jidc.append(tt)
        else:
                for tt in tbase:
                        if jid == tt[0] and tt[2].lower().count(text.lower())+tt[1].lower().count(text.lower()):
                                jidc.append(tt)                                

	for i in range(0,len(jidc)):
		for j in range(i,len(jidc)):
			if jidc[i][3] < jidc[j][3]:
				jj = jidc[i]
				jidc[i] = jidc[j]
				jidc[j] = jj

        if len(jidc)> 10:
                jidc = jidc[:10]

	maxlen = 0
	for tt in jidc:
		if len(tt[2])>maxlen:
			maxlen=len(tt[2])
	tabz = ''
	while maxlen >=0:
		tabz+='\t'
		maxlen -= tab_size

        msg = u'Болтуны:\nНик'+tabz+u'Слов\tФраз\tКоэф.'

        for tt in jidc:
		ml = len(tt[2])
		ttz = tabz
		while ml >= tab_size:
			ttz = ttz[:-1]
			ml -= tab_size
                msg += u'\n'+tt[2] +ttz+ str(tt[3]) +u'\t'+ str(tt[4]) + u'\t'+ str(float(int(float(tt[3])/float(tt[4])*100))/100)
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

global execute

execute = [(1, prefix+u'talkers', talkers, 2),
	   (1, prefix+u'gtalkers', gtalkers, 2)]
