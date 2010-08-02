#!/usr/bin/python
# -*- coding: utf-8 -*-

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
	except: smbl = GT('calendar_default_splitter')
	try:
		msg = L('\nMon Tue Wed Thu Fri Sat Sun\n')
		for tmp in calendar.monthcalendar(year, month):
			for tmp2 in tmp:
				if tmp2: msg+=add_space_to_number(tmp2)+' '
				else: msg+='   '
			msg = msg[:-1]+'\n'
		msg = L('Now: %s%s') % (timeadd(tuple(localtime())), msg[:-1].replace(' ',smbl))
	except: msg = L('Error!')
	send_msg(type, jid, nick, msg)
	
global execute

execute = [(3, 'calendar', month_cal, 2, L('Calendar. Without parameters show calendar for current month.\ncalendar [month][year][symbol_splitter]'))]
