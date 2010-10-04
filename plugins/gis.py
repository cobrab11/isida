#!/usr/bin/python
# -*- coding: utf -*-

def gweather_raw(type, jid, nick, text, fully):
	def get_date(body):
		tmp = get_tag_item(body,'FORECAST','day')+'.'+get_tag_item(body,'FORECAST','month')
		ytmp = get_tag_item(body,'FORECAST','year')
		if str(tuple(time.localtime())[0]) == ytmp: return tmp
		return tmp+'.'+ytmp
	def get_maxmin(body,tag,splitter):
		tmax = get_tag_item(body,tag,'max')
		tmin = get_tag_item(body,tag,'min')
		if not fully: return str(int((int(tmax)+int(tmin))/2))
		if tmax == tmin: return tmax
		if (int(tmin)+int(tmax))/2 == 0: return '0'
		return tmin + splitter + tmax
	def get_themp(body): return get_maxmin(body,'TEMPERATURE','..')
	def get_wind(body): return get_maxmin(body,'WIND','-')
	def get_pressure(body): return get_maxmin(body,'PRESSURE','-')
	def get_relwet(body): return get_maxmin(body,'RELWET','-')
		
	tods = {'0':L('Night'),'1':L('Morning'),'2':L('Day'),'3':L('Evening')}
	precipitation = {'4':L('rain'),'5':L('downpour'),'6':L('snow'),'7':L('snow'),'8':L('storm'),'9':L('no data'),'10':L('no precipitation')}
	cloudiness = {'0':L('clear'),'1':L('cloudy'),'2':L('Cloudy'),'3':L('overcast')}
	winddir = {'0':L('N'),'1':L('NE'),'2':L('E'),'3':L('SE'),'4':L('S'),'5':L('SW'),'6':L('W'),'7':L('NW')}

	if len(reduce_spaces(text)):
		text = text.lower()
		cbb = sqlite3.connect(gisbase)
		cu = cbb.cursor()
		wzc = cu.execute('select * from gis where code like ? or lcity like ?',(text,text)).fetchall()
		if not wzc:
			text = '%'+text+'%'
			wzc = cu.execute('select * from gis where code like ? or lcity like ?',(text,text)).fetchall()
		cbb.close()
		if wzc:
			if len(wzc) == 1:		
				text = wzc[0][0]
				link = 'http://informer.gismeteo.ru/xml/'+text+'.xml'
				try: body, noerr = html_encode(urllib.urlopen(link).read()), True
				except Exception, SM:
					try: body = str(SM)
					except: body = unicode(SM)
					noerr = None
				if noerr:
					body = body.split('<FORE')[1:]
					msg = L('Weather in %s:\nDate\t t%s\tWind\tClouds') % (wzc[0][1],u'°')
					if fully: msg += L('\tPressure, mm. Hg. Art.\tHumidity %')
					for tmp in body:
						tmp2 = '<FORE' + tmp
						msg += '\n' + tods[get_tag_item(tmp2,'FORECAST','tod')] + ' ' + get_date(tmp2)	# дата + время суток
						msg += '\t' + get_themp(tmp2) 													# температура
						gwi = get_wind(tmp2)															# ветер
						if gwi == '0': msg += L('\tCalm')
						else: msg += '\t' + gwi+' '+winddir[get_tag_item(tmp2,'WIND','direction')]
						msg += '\t' + cloudiness[get_tag_item(tmp2,'PHENOMENA','cloudiness')]			# облачность
						msg += ', ' + precipitation[get_tag_item(tmp2,'PHENOMENA','precipitation')]		# осадки
						if fully: msg += '\t' + get_pressure(tmp2) + '\t' + get_relwet(tmp2)			# давление, влажность
				else: msg = L('Error! %s') % body
			else:
				msg = L('Found:')
				for tmp in wzc: msg += '\n'+tmp[0]+' - '+tmp[1]
		else: msg = L('Not found.')
	else: msg = L('What?')
	send_msg(type, jid, nick, msg)

def gweather(type, jid, nick, text): gweather_raw(type, jid, nick, text, None)

def gweatherplus(type, jid, nick, text): gweather_raw(type, jid, nick, text, True)

global execute

execute = [(3, 'gis', gweather, 2, L('Weather forecast (short). Courtesy Gismeteo.Ru | http://www.gismeteo.ru')),
		   (3, 'gis+', gweatherplus, 2, L('Weather forecast (full). Courtesy Gismeteo.Ru | http://www.gismeteo.ru'))]
