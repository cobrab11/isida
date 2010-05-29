#!/usr/bin/python
# -*- coding: utf -*-

def check_wz(text):
	if not len(text): return True
	for tm in text:
		if ord(tm)<33 or ord(tm)>127: return True
	return None

def get_weather(text):
	cbb = sqlite3.connect(wzbase)
	cu = cbb.cursor()
	wzc = cu.execute('select code from wz where code like ? or city like ? or counry like ?',(text,text,text)).fetchall()
	cbb.close()
	if not wzc: return 'Not Found'
	if len(wzc) != 1: return 'Not Found'
	text = wzc[0][0].upper()
	link = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/'+text+'.TXT'
	f = urllib.urlopen(link)
	wzz = f.read()
	f.close()
	return wzz

def weather(type, jid, nick, text):
	if check_wz(text): msg = L('Error in parameters. Read the help about command.')
	else:
		wzz = get_weather(text)
		if wzz.count('Not Found'): msg = L('City not found!')
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
	if check_wz(text): msg = L('Error in parameters. Read the help about command.')
	else:
		wzz = get_weather(text)
		if wzz.count('Not Found'): msg = L('City not found!')
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
	if check_wz(text): msg = L('Error in parameters. Read the help about command.')
	else:
		msg = get_weather(text)[:-1]
		if msg.count('Not Found'): msg = L('City not found!')
	send_msg(type, jid, nick, msg)

def weather_search(type, jid, nick, text):
	if len(text):
		cbb = sqlite3.connect(wzbase)
		cu = cbb.cursor()
		wzc = cu.execute('select code,city,counry from wz where code like ? or city like ? or counry like ?',(text,text,text)).fetchall()
		cbb.close()
		if not wzc: msg = msg = L('City not found!')
		else:
			msg = ''
			for tmp in wzc: msg += '\n%s - %s (%s)' % tmp
			msg = L('Found: %s') % msg
	else: msg = L('What?')
	send_msg(type, jid, nick, msg)
	
global execute

execute = [(0, 'wzz', weather_raw, 2, L('Weather by airport code. Full version.')),
	 (0, 'wzs', weather_short, 2, L('Weather by airport code. Short version.')),
	 (0, 'wz', weather, 2, L('Weather by airport code. Optimized version.')),
	 (0, 'wzsearch', weather_search, 2, L('Search weather by code, city, country.'))]
