#!/usr/bin/python
# -*- coding: utf -*-

def get_holiday(sdate):

	''' Function get holiday from file plugins/date.txt and return title of
	holiday if holiday found, else return empty unicode message. Input params
	must be	list of int

	:[month, day]:'''

	result = ''
	date_base = readfile(date_file).decode('UTF').split('\n')
	for ddate in date_base:
		if ddate != '\n' or ddate != '':
			ddate = ddate.split('-')
			hdate = ddate[0]
			if hdate.count('.'):
				hdate = map(int, hdate.split('.'))
				hdate.reverse()
				if hdate == sdate:
					result += ddate[1].strip() + ', '
	if len(result) > 2: result = result[:-2]
	return result

def parse_date_string(string_date, spl='.'):
	
	''' Parse date string and return list [year, month, day] ''' 
	
	date_formats = ['%d'+spl+'%m', '%d'+spl+'%m'+spl+'%y',
		'%d'+spl+'%m'+spl+'%Y', '%Y'+spl+'%m'+spl+'%d']
	#output = list(localtime())[:3]
	for format in date_formats:
		try: output = list(time.strptime(string_date, format))[:3]
		except: pass
	return output

def to_date(type, jid, nick, text):
	dmass = (L('days'), L('day'), L('Days').lower(), L('Days').lower(), 
		L('Days').lower(), L('days'), L('days'), L('days'), L('days'), L('days'))
	splitters = ('.', '-', ':', '/', ',', '\\')
	if len(text):
		#try:
			spl = [spl for spl in splitters if text.count(spl)][0]
			sdate = parse_date_string(text, spl)
			if sdate[0] == 1900: sdate[0] = list(localtime())[0]
			year = sdate.pop(0)
			month, day = sdate
			hday = get_holiday(sdate)
			text = text.replace(spl, '.')
			msg = ''
			if len(hday) > 0: text = hday
			days_remain = (datetime.date(year, month, day) - datetime.date.today()).days
			if len(str(abs(days_remain))) > 1 and str(days_remain)[-2] == '1':
				dmass = (L('days'),L('days'),L('days'),L('days'),
					L('days'),L('days'),L('days'),L('days'),
					L('days'),L('days'))
			if days_remain < 0: msg += L('was %s %s ago') % \
				(str(abs(days_remain)), dmass[int(str(days_remain)[-1])])
			elif  days_remain == 0: msg += L('today')
			else: msg += L('will be in %s %s') % \
				(str(abs(days_remain)), dmass[int(str(days_remain)[-1])])
			msg = text + ' ' + msg
#		except: msg = L('Error in parameters. Read the help about command.')
	else: msg = L('Error in parameters. Read the help about command.')
	send_msg(type, jid, nick, msg)

def todate(type, jid, nick, text):
	dmass = (L('days'), L('day'), L('Days').lower(), L('Days').lower(),
		L('Days').lower(), L('days'), L('days'), L('days'), L('days'), L('days'))
	splitters = ('.', '-', ':', '/', ',', '\\')
	msg = ''
	if len(text):
		try:
			if text.count(' '): ddate, msg = text.split(' ', 1)[0], text.split(' ', 1)[1]
			else: ddate = text
			spl = [spl for spl in splitters if ddate.count(spl)][0]
			if len(msg) == 0: msg = L('before the %s remained') % ddate.replace(spl, '.')
			sdate = parse_date_string(ddate, spl)
			if sdate[0] == 1900: sdate[0] = list(localtime())[0]
			year = sdate.pop(0)
			month, day = sdate
			days_remain = (datetime.date(year, month, day) - datetime.date.today()).days
			if len(str(abs(days_remain))) > 1 and str(days_remain)[-2] == '1':
				dmass = (L('days'),L('days'),L('days'),L('days'),
					L('days'),L('days'),L('days'),L('days'),
					L('days'),L('days'))
			if days_remain < 0: msg = L('Date has already in past!')
			else: msg += ' ' + str(days_remain) + ' ' + dmass[int(str(days_remain)[-1])]
		except: msg = L('Error in parameters. Read the help about command.')
	else: msg = L('Error in parameters. Read the help about command.')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'to_date', to_date, 2, L('Calculate count of days for requested date, if the date is holiday, that returned title of holiday.\nSupported date formats: dd.mm.yyyy, dd.mm, dd.mm.yy, yyyy.mm.dd\nSupported splitters: ,-.:/\\\ntodate 05.09\ntodate 5/9/2010')),
	(3, 'todate', todate, 2, L('Calculate count of days for requested date.\nSupported date formats: dd.mm.yyyy, dd.mm, dd.mm.yy, yyyy.mm.dd\nSupported splitter: ,-.:/\\\ntodate 05.09 before New year remained\ntodate 5/9/2010 before New year remained'))]
