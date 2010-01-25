#!/usr/bin/python
# -*- coding: utf -*-

gisbase = set_folder+u'gis.db'

def gweather_raw(type, jid, nick, text, fully):
	def get_date(body):
		tmp = get_tag_item(body,'FORECAST','day')+'.'+get_tag_item(body,'FORECAST','month')
		ytmp = get_tag_item(body,'FORECAST','year')
		if str(tuple(time.localtime())[0]) == ytmp: return tmp
		return tmp+'.'+ytmp
	def get_maxmin(body,tag,splitter):
		tmax = get_tag_item(body,tag,'max')
		tmin = get_tag_item(body,tag,'min')
		if not fully: return str((int(tmax)+int(tmin))/2)
		if tmax == tmin: return tmax
		return tmin + splitter + tmax
	def get_themp(body): return get_maxmin(body,'TEMPERATURE','..')
	def get_wind(body): return get_maxmin(body,'WIND','-')
	def get_pressure(body): return get_maxmin(body,'PRESSURE','-')
	def get_relwet(body): return get_maxmin(body,'RELWET','-')
		
	tods = {'0':u'Ночь','1':u'Утро','2':u'День','3':u'Вечер'}
	precipitation = {'4':u'дождь','5':u'ливень','6':u'снег','7':u'снег','8':u'гроза','9':u'нет данных','10':u'без осадков'}
	cloudiness = {'0':u'ясно','1':u'малооблачно','2':u'облачно','3':u'пасмурно'}
	winddir = {'0':u'С','1':u'СВ','2':u'В','3':u'ЮВ','4':u'Ю','5':u'ЮЗ','6':u'З','7':u'СЗ'}

	if len(reduce_spaces(text)):
		text = '%'+text.lower()+'%'
		cbb = sqlite3.connect(gisbase)
		cu = cbb.cursor()
		wzc = cu.execute('select * from gis where code like ? or lcity like ?',(text,text)).fetchall()
		cbb.close()
		if wzc:
			if len(wzc) == 1:		
				text = wzc[0][0]
				link = 'http://informer.gismeteo.ru/xml/'+text+'.xml'
				try: body, noerr = html_encode(urllib.urlopen(link).read()), True
				except Exception, SM: body, noerr = str(SM), None
				if noerr:
					body = body.split('<FORE')[1:]
					msg = u'Погода в городе '+wzc[0][1]+u':\nДата\t t°\tВетер\tОблачность'
					if fully: msg += u'\tДавление, мм.рт.ст.\tВлажность %'
					for tmp in body:
						tmp2 = '<FORE' + tmp
						msg += u'\n' + tods[get_tag_item(tmp2,'FORECAST','tod')] + ' ' + get_date(tmp2)	# дата + время суток
						msg += '\t' + get_themp(tmp2) 													# температура
						msg += '\t' + get_wind(tmp2)+' '+winddir[get_tag_item(tmp2,'WIND','direction')]	# ветер
						msg += '\t' + cloudiness[get_tag_item(tmp2,'PHENOMENA','cloudiness')]			# облачность
						msg += ', ' + precipitation[get_tag_item(tmp2,'PHENOMENA','precipitation')]		# осадки
						if fully: msg += '\t' + get_pressure(tmp2) + '\t' + get_relwet(tmp2)			# давление, влажность
				else: msg = u'Ошибка: '+body
			else:
				msg = u'Найдено:'
				for tmp in wzc: msg += u'\n'+tmp[0]+u' - '+tmp[1]
		else: msg = u'Не найдено!'
	else: msg = u'Ась?'
	send_msg(type, jid, nick, msg)

def gweather(type, jid, nick, text): gweather_raw(type, jid, nick, text, None)

def gweatherplus(type, jid, nick, text): gweather_raw(type, jid, nick, text, True)

global execute

execute = [(0, u'gis', gweather, 2, u'Краткий прогноз погоды. Предоставлено Gismeteo.Ru | http://www.gismeteo.ru'),
		   (0, u'gis+', gweatherplus, 2, u'Полный прогноз погоды. Предоставлено Gismeteo.Ru | http://www.gismeteo.ru')]
