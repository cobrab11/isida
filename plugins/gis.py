#!/usr/bin/python
# -*- coding: utf -*-

def weather_gis(type, jid, nick, text):
	city_code = None
	if text == '':
		msg = u'gis город|код города'
	else:
		try:
			city_code = str(int(text))
		except:
			ft = ''
			for tex in text:
				if ord(tex) == 32:
					ft += '%20'
				elif ord(tex)<127:
					ft += tex
				else:
					ft += hex(ord(tex.upper())-1040+192).replace('0x','%').upper()
			link = 'http://wap.gismeteo.ru/gm/normal/node/search_result/6/?like_field_sname='+ft
			f = urllib.urlopen(link)
			body = f.read()
			f.close()
			try:
				body = unicode(body.split('<br>')[1],'utf-8').split('field_index=')[1:]
				giss = []
				for tmp in body:
					giss.append((tmp.split('&')[0],tmp.split('gen_past_date_0">')[1].split('</a>')[0]))
				if len(giss) == 1:
					city_code = giss[0][0]
				elif len(giss) == 0:
					msg = u'Город '+text+u' не найден!'
				else:
					msg = u'Найдено больше одного города! Воспользуйтесь командой gis код_города'
					for tmp in giss:
						msg += u'\n'+tmp[0]+u' — '+tmp[1]
			except:
				if body.lower().count(u'forbidden'):
					msg = u'Доступ к серверу погоды запрещён на стороне сервера.'
				else:
					msg = u'К сожалению сервер не отвечает.'
	if city_code:
		link = 'http://wap.gismeteo.ru/gm/normal/node/prognoz_type/6/?field_wmo='+city_code+'&field_index='+city_code+'&sd_field_date=gen_past_date_0&ed_field_date=gen_past_date_0'
		f = urllib.urlopen(link)
		body = f.read()
		f.close()
		body = html_encode(body)
		body = replacer(body)
		body = body.split('#006cb7')[3]
		body = body.replace(u',  м/с',u' ')
		body = body.replace(u'безветрие',u'штиль')
		b = body.split('\n')
		if b[7] == u'На неделю':
			b.insert(5,'')
		if len(b[5]):
			msg = b[6]+', '+b[5]+', '+b[4]+' ('+b[1]+')'
		else:
			msg = b[6]+', '+b[4]+' ('+b[1]+')'
		msg += u'\n\tt°C\tДавл.\tВлажн.\tВетер'
		ms = ['']
		ms.append(u'\nНочь:\t'+b[12]+'\t'+b[14]+'\t'+b[16]+'\t'+b[18]+b[19]+'\t'+b[10]+', '+b[11])
		ms.append(u'\nУтро:\t'+b[22]+'\t'+b[24]+'\t'+b[26]+'\t'+b[28]+b[29]+'\t'+b[20]+', '+b[21])
		ms.append(u'\nДень:\t'+b[32]+'\t'+b[34]+'\t'+b[36]+'\t'+b[38]+b[39]+'\t'+b[30]+', '+b[31])
		ms.append(u'\nВечер:\t'+b[42]+'\t'+b[44]+'\t'+b[46]+'\t'+b[48]+b[49]+'\t'+b[40]+', '+b[41])

		link = 'http://wap.gismeteo.ru/gm/normal/node/prognoz_tomorrow/6/?field_wmo='+city_code+'&field_index='+city_code+'&sd_field_date=gen_past_date_-1&ed_field_date=gen_past_date_-1'
		f = urllib.urlopen(link)
		body = f.read()
		f.close()
		body = html_encode(body)
		body = replacer(body)
		body = body.split('#006cb7')[3]
		body = body.replace(u',  м/с',u' ')
		body = body.replace(u'безветрие',u'штиль')
		b = body.split('\n')
		if b[7] == u'На неделю':
			b.insert(5,'')
		ms.append(u'\nНочь:\t'+b[12]+'\t'+b[14]+'\t'+b[16]+'\t'+b[18]+b[19]+'\t'+b[10]+', '+b[11])
		ms.append(u'\nУтро:\t'+b[22]+'\t'+b[24]+'\t'+b[26]+'\t'+b[28]+b[29]+'\t'+b[20]+', '+b[21])
		ms.append(u'\nДень:\t'+b[32]+'\t'+b[34]+'\t'+b[36]+'\t'+b[38]+b[39]+'\t'+b[30]+', '+b[31])
		ms.append(u'\nВечер:\t'+b[42]+'\t'+b[44]+'\t'+b[46]+'\t'+b[48]+b[49]+'\t'+b[40]+', '+b[41])
		
		beg = tuple(localtime())[3]/4
		for tmp in ms[beg:beg+4]:
			msg += tmp
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'gis', weather_gis, 2, u'Погода с GisMeteo.\ngis город|код_города')]
