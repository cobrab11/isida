#!/usr/bin/python
# -*- coding: utf -*-

user_agent='Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'

def gis_append(ms,b):
	cr = 9 # корректор смещения при смене разметки
	ms.append(u'\nНочь:\t'+b[cr+2]+'\t'+b[cr+4]+'\t'+b[cr+6]+'\t'+b[cr+8]+b[cr+9]+'\t'+b[cr]+', '+b[cr+1])
	ms.append(u'\nУтро:\t'+b[cr+12]+'\t'+b[cr+14]+'\t'+b[cr+16]+'\t'+b[cr+18]+b[cr+19]+'\t'+b[cr+10]+', '+b[cr+11])
	ms.append(u'\nДень:\t'+b[cr+22]+'\t'+b[cr+24]+'\t'+b[cr+26]+'\t'+b[cr+28]+b[cr+29]+'\t'+b[cr+20]+', '+b[cr+21])
	ms.append(u'\nВечер:\t'+b[cr+32]+'\t'+b[cr+34]+'\t'+b[cr+36]+'\t'+b[cr+38]+b[cr+39]+'\t'+b[cr+30]+', '+b[cr+31])
	return ms
	
def gis_get_day(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent',user_agent)
	try:
		body = urllib2.urlopen(req).read()
		b = replacer(html_encode(body)).split('#006cb7')[3].replace(u',  м/с',u' ').replace(u'безветрие',u'штиль').split('\n')
	except: b = u'forbidden'
	return b
	
def weather_gis(type, jid, nick, text):
	city_code = None
	if text == '': msg = u'gis город|код города'
	else:
		try: city_code = str(int(text))
		except:
			ft = ''
			for tex in text:
				if ord(tex) == 32: ft += '%20'
				elif ord(tex)<127: ft += tex
				else: ft += hex(ord(tex.upper())-1040+192).replace('0x','%').upper()
			url = 'http://wap.gismeteo.ru/gm/normal/node/search_result/6/?like_field_sname='+ft
			req = urllib2.Request(url)
			req.add_header('User-Agent',user_agent)
			try: body = urllib2.urlopen(req).read()
			except: body = u'forbidden'
			try:
				body = unicode(body.split('<br>')[1],'utf-8').split('field_index=')[1:]
				giss = []
				for tmp in body: giss.append((tmp.split('&')[0],tmp.split('gen_past_date_0">')[1].split('</a>')[0]))
				if len(giss) == 1: city_code = giss[0][0]
				elif len(giss) == 0: msg = u'Город '+text+u' не найден!'
				else:
					msg = u'Найдено больше одного города! Воспользуйтесь командой gis код_города'
					for tmp in giss: msg += u'\n'+tmp[0]+u' — '+tmp[1]
			except:
				if body.lower().count(u'forbidden'): msg = u'Доступ к серверу погоды запрещён на стороне сервера.'
				else: msg = u'К сожалению сервер не отвечает.'
	if city_code:
		b = gis_get_day('http://wap.gismeteo.ru/gm/normal/node/prognoz_type/6/?field_wmo='+city_code+'&field_index='+city_code+'&sd_field_date=gen_past_date_0&ed_field_date=gen_past_date_0')
		if b == u'forbidden': msg = u'Доступ к серверу погоды запрещён на стороне сервера.'
		else:
			if b[5].lower().count(u'завтра'):
				msg = b[4]+', '+b[3]+' ('+b[1]+')'
				b.insert(0,'')
			else: msg = b[5]+', '+b[4]+', '+b[3]+' ('+b[1]+')'
			msg += u'\n\tt°C\tДавл.\tВлажн.\tВетер'
			ms = gis_append([''],b)
			b = gis_get_day('http://wap.gismeteo.ru/gm/normal/node/prognoz_tomorrow/6/?field_wmo='+city_code+'&field_index='+city_code+'&sd_field_date=gen_past_date_-1&ed_field_date=gen_past_date_-1')
			if b[5].lower().count(u'завтра'): b.insert(0,'')
			ms = gis_append(ms,b)
			beg = tuple(localtime())[3]/4+1
			for tmp in ms[beg:beg+4]: msg += tmp
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'gis', weather_gis, 2, u'Погода с GisMeteo.\ngis город|код_города')]
