# -*- coding: utf-8 -*-

import datetime

def get_holiday(sdate):

	''' Function get holiday from file plugins/date.txt and return title of
	holiday if holiday found, else return empty unicode message. Input params
	must be	list of int

	:[month, day]:'''

	result = u''
	date_file = 'plugins/date.txt'
	date_base = readfile(date_file).decode('UTF').split('\n')
	for ddate in date_base:
		if ddate != '\n' or ddate != '':
			ddate = ddate.split('-')
			hdate = ddate[0]
			if hdate.count('.'):
				hdate = map(int, hdate.split('.'))
				hdate.reverse()
				if hdate == sdate:
					result += ddate[1].strip() + u', '
	if len(result) > 2: result = result[:-2]
	return result

def parse_date_string(string_date, spl='.'):
	
	''' Parse date string and return list [year, month, day] ''' 
	
	date_formats = ['%d'+spl+u'%m', '%d'+spl+u'%m'+spl+u'%y',
		'%d'+spl+u'%m'+spl+u'%Y', '%Y'+spl+u'%m'+spl+u'%d']
	#output = list(localtime())[:3]
	for format in date_formats:
		try: output = list(time.strptime(string_date, format))[:3]
		except: pass
	return output

def to_date(type, jid, nick, text):
	dmass = (u'дней', u'день', u'дня', u'дня', u'дня', u'дней', u'дней',
		u'дней', u'дней', u'дней')
	splitters = (u'.', u'-', u':', u'/', u',', u'\\')
	if len(text):
		try:
			spl = [spl for spl in splitters if text.count(spl)][0]
			sdate = parse_date_string(text, spl)
			if sdate[0] == 1900: sdate[0] = list(localtime())[0]
			year = sdate.pop(0)
			month, day = sdate
			hday = get_holiday(sdate)
			text = text.replace(spl, '.')
			msg = u''
			if len(hday) > 0: text = hday
			days_remain = (datetime.date(year, month, day) - datetime.date.today()).days
			if len(str(abs(days_remain))) > 1 and str(days_remain)[-2] == '1':
				dmass = (u'дней', u'дней', u'дней', u'дней', u'дней', u'дней',
					u'дней', u'дней', u'дней', u'дней')
			if days_remain < 0: msg += u' был(и/о) ' + str(abs(days_remain)) + u' ' + \
				dmass[int(str(days_remain)[-1])] + u' назад'
			elif  days_remain == 0: msg += ' сегодня'
			else: msg += u' будет через ' + str(abs(days_remain)) + u' ' + \
				dmass[int(str(days_remain)[-1])]
			msg = text + msg
		except: msg = u'Ошибка в параметрах команды, прочитайте помощь по команде.'
	else: msg = u'Ошибка в параметрах команды, прочитайте помощь по команде.'
	send_msg(type, jid, nick, msg)

def todate(type, jid, nick, text):
	dmass = (u'дней', u'день', u'дня', u'дня', u'дня', u'дней', u'дней',
		u'дней', u'дней', u'дней')
	splitters = (u'.', u'-', u':', u'/', u',', u'\\')
	msg = u''
	if len(text):
		try:
			if text.count(' '): ddate, msg = text.split(' ', 1)[0], text.split(' ', 1)[1]
			else: ddate = text
			spl = [spl for spl in splitters if ddate.count(spl)][0]
			if len(msg) == 0: msg = u'До ' + ddate.replace(spl, '.') + u' осталось'
			sdate = parse_date_string(ddate, spl)
			if sdate[0] < tuple(localtime())[0]: sdate[0] = list(localtime())[0]
			year = sdate.pop(0)
			month, day = sdate
			days_remain = (datetime.date(year, month, day) - datetime.date.today()).days
			if len(str(abs(days_remain))) > 1 and str(days_remain)[-2] == '1':
				dmass = (u'дней', u'дней', u'дней', u'дней', u'дней', u'дней',
					u'дней', u'дней', u'дней', u'дней')
			if days_remain < 0: msg = u'Ошибка формата даты'
			else: msg += u' ' + str(days_remain) + u' ' + dmass[int(str(days_remain)[-1])]
		except: msg = u'Ошибка в параметрах команды, прочитайте помощь по команде.'
	else: msg = u'Ошибка в параметрах команды, прочитайте помощь по команде.'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'to_date', to_date, 2, u'Рассчет количества дней от текущей даты до заданной, если на заданную дату выпадает праздник, то возвращается название праздника вместо запрашиваемой даты\nПоддерживаемые форматы даты: dd.mm.yyyy, dd.mm, dd.mm.yy, yyyy.mm.dd\nПоддерживаемые разделители: ,-.:/\\\ntodate 05.09\ntodate 5/9/2010'),
	(0, u'todate', todate, 2, u'Рассчет количества дней от текущей даты до заданной, с возможностью вставки собственного текста\nПоддерживаемые форматы даты: dd.mm.yyyy, dd.mm, dd.mm.yy, yyyy.mm.dd\nПоддерживаемые разделители: ,-.:/\\\ntodate 05.09 До дня победы осталось\ntodate 5/9/2010 До дня победы осталось')]