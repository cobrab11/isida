#!/usr/bin/python
# -*- coding: utf -*-

def weather(type, jid, nick, text):
	for tm in text:
		if ord(tm)<33 or ord(tm)>127:
			send_msg(type, jid, nick, u'Ошибка в параметрах!')
			return
	text = text.upper()
	link = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/'+text+'.TXT'
	f = urllib.urlopen(link)
	wzz = f.read()
	f.close()

	if wzz.count('Not Found'): msg = u'Город не найден!'
	else:
		wzz = wzz.split('\n')

		wzr = []
		wzr.append(wzz[0])			# 0
		wzr.append(wzz[1])			# 1
		wzr.append(sfind(wzz,'Temperature'))	# 2
		wzr.append(sfind(wzz,'Wind'))		# 3
		wzr.append(sfind(wzz,'Relative'))	# 4
		wzr.append(sfind(wzz,'Sky'))		# 5
		wzr.append(sfind(wzz,'Weather'))	# 6
		wzr.append(sfind(wzz,'Visibility'))	# 7
		wzr.append(sfind(wzz,'Pressure'))	# 8

		if wzr[0].count(')'): msg = wzr[0][:wzr[0].find(')')+1]
		else: msg = wzr[0]
		msg += '\n'+ wzr[1]

		wzz1 = wzr[2].find(':')+1 # Temperature
		wzz2 = wzr[2].find('(',wzz1)
		wzz3 = wzr[2].find(')',wzz2)
		msg += '\n'+ wzr[2][:wzz1] + ' ' + wzr[2][wzz2+1:wzz3]

		wzz1 = wzr[3].find('(')
		wzz2 = wzr[3].find(')',wzz1)
		wzz3 = wzr[3].find(':',wzz2)
		msg += '\n'+ wzr[3][:wzz1-1] + wzr[3][wzz2+1:wzz3]

		msg += '\n'+ wzr[4]
		if len(wzr[5]): msg += ','+ wzr[5][wzr[5].find(':')+1:]
		if len(wzr[6]): msg += ','+ wzr[6][wzr[6].find(':')+1:]
		if not (len(wzr[5])+len(wzr[6])): msg += ', clear'

		msg += '\n'+ wzr[7][:-2]
		
		wzz1 = wzr[8].find('(')
		wzz2 = wzr[8].find(':',wzz1)
		wzz3 = wzr[8].find('(',wzz2)
		msg += ', '+ wzr[8][:wzz1-1]+': '+wzr[8][wzz3+1:-1]

	send_msg(type, jid, nick, msg)

def weather_short(type, jid, nick, text):
	for tm in text:
		if ord(tm)<33 or ord(tm)>127:
			send_msg(type, jid, nick, u'Ошибка в параметрах!')
			return
	text = text.upper()
	link = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/'+text+'.TXT'
	f = urllib.urlopen(link)
	wzz = f.read()
	f.close()

	if wzz.count('Not Found'): msg = u'Город не найден!'
	else:
		wzz = wzz.split('\n')

		wzr = []
		wzr.append(wzz[0])			# 0
		wzr.append(sfind(wzz,'Temperature'))	# 2
		wzr.append(sfind(wzz,'Wind'))		# 3
		wzr.append(sfind(wzz,'Relative'))	# 4
		wzr.append(sfind(wzz,'Sky'))		# 5
		wzr.append(sfind(wzz,'Weather'))	# 6

		if wzr[0].count(')'): msg = wzr[0][:wzr[0].find(')')+1]
		else: msg = wzr[0]

		wzz1 = wzr[1].find(':')+1 # Temperature
		wzz2 = wzr[1].find('(',wzz1)
		wzz3 = wzr[1].find(')',wzz2)
		msg += ' | '+ wzr[1][:wzz1] + ' ' + wzr[1][wzz2+1:wzz3]

		wzz1 = wzr[2].find('(')
		wzz2 = wzr[2].find(')',wzz1)
		wzz3 = wzr[2].find(':',wzz2)
		msg += ' | '+ wzr[2][:wzz1-1] + wzr[2][wzz2+1:wzz3]
		msg += ' | '+ wzr[3]
		if len(wzr[4]): msg += ','+ wzr[4][wzr[4].find(':')+1:]
		if len(wzr[5]): msg += ','+ wzr[5][wzr[5].find(':')+1:]
		if not (len(wzr[4])+len(wzr[5])): msg += ', clear'
	send_msg(type, jid, nick, msg)

def weather_raw(type, jid, nick, text):
	for tm in text:
		if ord(tm)<33 or ord(tm)>127:
			send_msg(type, jid, nick, u'Ошибка в параметрах!')
			return
	text = text.upper()
	link = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/'+text+'.TXT'
	f = urllib.urlopen(link)
	msg = f.read()
	f.close()
	msg = msg[:-1]
	if msg.count('Not Found'): msg = u'Город не найден!'
	send_msg(type, jid, nick, msg)

def weather_city(type, jid, nick, text):
	for tm in text:
		if ord(tm)<32 or ord(tm)>127:
			send_msg(type, jid, nick, u'Ошибка в параметрах!')
			return
	text = text.upper()
	text = text.split(' ')

	link = 'http://weather.noaa.gov/weather/'+text[0]+'_cc.html'
	f = urllib.urlopen(link)
	wzz = f.read()
	f.close()

	if wzz.count('Not Found'): msg = u'Я не знаю такой страны!'
	else:
		wzpos = wzz.find('<select name=\"cccc\">')
		wzz = wzz[wzpos:wzz.find('</select>',wzpos)]

		wzz = wzz.split('<OPTION VALUE=\"')
		msg = u'Города по запросу: '
		not_add = 1
		for wzzz in wzz:
			if wzzz.lower().count(text[1].lower()):
				msg += '\n'+wzzz.replace('\">',' -')[:-1]
				not_add = 0
		if not_add: msg = u'Такой город не найден!'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'wzcity', weather_city, 2, u'Поиск кода города для запроса погоды.\nwzcity страна город, где страна - двухбуквенное сокращание, например ru или ua, город - фрагмент названия города.'),
	 (0, u'wzz', weather_raw, 2, u'Погода по коду аэропорта. Не оптимизированный вариант.'),
	 (0, u'wzs', weather_short, 2, u'Погода по коду аэропорта. Укороченный вариант.'),
	 (0, u'wz', weather, 2, u'Погода по коду аэропорта. Оптимизированный вариант.')]
