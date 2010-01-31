#!/usr/bin/python
# -*- coding: utf -*-

def gettelcode(text):
	query = urllib.urlencode({'text' : text.encode("windows-1251")})
	url = u'http://www.telcode.ru/mob/select.asp?%s'.encode("utf-8") % (query)
	f = urllib.urlopen(url)
	body = f.read()
	f.close()
	body = html_encode(body)
	if body.count(u'Не найдено записей'): return u'Не найдено!'
	else:
		msg = rss_del_html(get_tag(body,'h3'))+' ... '
		city = body.replace('\n','').replace('\r','').split('</h3>')[1].split('<br> <br>')[0].split('<br>')
		for tmp in city: msg += get_tag(tmp,'a')+', '
		msg = msg[:-2]
		return msg

def gettcode(text):
	try: csize = int(text.split('\n')[1])
	except: csize = 3
	if csize < 1: csize = 1
	elif csize > 25: csize = 25
	text = text.split('\n')[0]
	try: url = u'http://www.btk-online.ru/phcode/?srchCId=1&srchTName=&srchCCode=&srchTCode='+str(int(text))
	except: url = u'http://www.btk-online.ru/phcode/?srchCId=1&%s'.encode("utf-8") % (urllib.urlencode({'srchTName': text.encode("windows-1251")}))
	user_agent='Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'
	req = urllib2.Request(url)
	req.add_header('User-Agent',user_agent)
	body = urllib2.urlopen(req).read()
	body = html_encode(body)
	if body.count('<table id=pcodephones cellspacing=0>\n  <tr><th width'): return u'По вашему запросу ничего не найдено.'
	else:
		body = body.split('<table id=pcodephones cellspacing=0>')[1].split('</table>')[0].split('</tr>')[1:]
		if body != [u'\n ']:
			msg = u'Найдено:'
			for tmp in body[:csize]:
				tmp2 = '\n'+replacer(tmp).replace('\n',', ').replace(';',', ')
				tmp3 = tmp2[tmp2.find(u' тариф'):tmp2.find(u',',tmp2.find(u' тариф'))+1]
				msg += tmp2.replace(tmp3,'')
			return msg
		else: return u'По вашему запросу ничего не найдено.'
	
def getdefcode(text):
	ddef = text[1:4]
	dnumber = text[4:]
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
	if msg[0].count(u'не найдено'): return u'Не найдено!'
	else:
		msg.remove(msg[0])
		mmsg = u'Найдено:\n'
		for mm in msg:
			tmm = mm
			tmm = replacer(tmm)
			tmm = tmm[tmm.find('>')+1:]
			tmm = tmm.replace('\n','\t')
			mmsg += tmm[2:] + '\n'
		msg = mmsg[:-1]
		return msg

def phonecode(type, jid, nick, text):
	if len(text):
		if text[0] == '+': text = text[1:]
		if text[:2] == '79': msg = getdefcode(text[:7])
		else:
			try: msg = gettelcode(str(int(text)))
			except: msg = gettcode(text)
	else: msg = u'Ась?'
   	send_msg(type, jid, nick, msg)
		
global execute

execute = [(0, u'phone', phonecode, 2, u'Информация о коде города, DEF коде, поиск кода по названию')]
