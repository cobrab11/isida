#!/usr/bin/python
# -*- coding: utf-8 -*-

import calendar

def add_space_to_number(num):
	if num<10: return ' '+str(num)
	else: return str(num)

def month_cal(type, jid, nick, text):
	text = text.split()
	try: month = int(text[0])
	except: month = tuple(localtime())[1]
	try: year = int(text[1])
	except: year = tuple(localtime())[0]
	try: smbl = text[2]
	except: smbl = ' '
	try:
		msg = u'\nПн Вт Ср Чт Пт Сб Вс\n'
		for tmp in calendar.monthcalendar(year, month):
			for tmp2 in tmp:
				if tmp2: msg+=add_space_to_number(tmp2)+' '
				else: msg+='   '
			msg = msg[:-1]+'\n'
		msg = u'Сейчас: '+timeadd(tuple(localtime()))+msg[:-1].replace(' ',smbl)
	except: msg = u'Ошибка!'
	send_msg(type, jid, nick, msg)
	
global execute

execute = [(0, u'calendar', month_cal, 2, u'Показ календаря. Без параметров показывает календарь на текущий месяц\ncalendar [месяц][год][символ_разделитель]')]
