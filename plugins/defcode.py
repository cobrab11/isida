#!/usr/bin/python
# -*- coding: utf -*-

def defcode(type, jid, nick, text):
	dcnt = text[0]
	ddef = text[1:4]
	dnumber = text[4:]
	if text[:2] != '79': msg = u'Поиск только по мобильным телефонам России!'
	else:
		link = 'http://www.mtt.ru/info/def/index.wbp?def='+ddef+'&number='+dnumber+'&region=&standard=&date=&operator='
		f = urllib.urlopen(link)
		msg = f.read()
		f.close()

		encidx = msg.find('charset=')
		if encidx >= 0:
			enc = msg[encidx+8:encidx+30]
			enc = enc[:enc.index('\">')]
			enc = enc.upper()
		else: enc = 'UTF-8'

		msg = unicode(msg, enc)

		mbeg = msg.find('<INPUT TYPE=\"submit\" CLASS=\"submit\"')
		msg = msg[mbeg:msg.find('</table>',mbeg)]
		msg = msg.split('<tr')
		
		if msg[0].count(u'не найдено'): msg = u'Не найдено!'
		else:
			msg.remove(msg[0])
			mmsg = u'Найдено:\n'
			for mm in msg:
				tmm = mm
				tmm = replacer(tmm)
				tmm = tmm[tmm.find('>')+1:]
				tmm = tmm.replace('\n','\t')
				mmsg += tmm[1:-2] + '\n'
			msg = mmsg[:-1]
	
       	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'def', defcode, 2, u'Территориальная пренадлежность номера мобильного телефона. Внимание! Указывайте не менее 7 первых цифр номера во избежании большого количества сообщений!')]
