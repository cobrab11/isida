#!/usr/bin/python
# -*- coding: utf -*-

def to_drink(type, jid, nick, text):
	dmas = [L('first'),L('second'),L('third'),L('fourth'),L('fifth'),L('sixth'),L('seventh'),L('eighth'),L('nineth'),L('tenth'),
		L('eleventh'),L('twelveth'),L('thirteenth'),L('fourteenth'),L('fivteenth'),L('sixteenth'),
		L('seventeenth'),L('eighteenth'),L('nineteenth'),('twentieth'),L('twenty-first'),L('twenty-second'),
		L('twenty-third'),L('twenty-fourth'),L('twenty-fifth'),L('twenty-sixth'),L('twenty-seventh'),
		L('twenty-eighth'),L('twenty-nineth'),L('thirtieth'),L('thirty-first')]
	mmas1 = [L('january'),L('february'),L('march'),L('april'),L('may'),L('june'),L('july'),L('august'),
		L('september'),L('october'),L('november'),L('december')]
	mmas2 = [L('January'),L('February'),L('March'),L('April'),L('May'),L('June'),L('July'),L('August'),
		L('September'),L('October'),L('November'),L('December')]
	wday = [L('monday'),L('tuesday'),L('wendesday'),L('thirsday'),L('friday'),L('saturday'),L('sunday')]
	lday = [L('last').lower(),L('last').lower(),L('Last').lower(),
		L('last').lower(),L('Last').lower(),L('Last').lower(),L('lAst').lower()]
	date_file = 'plugins/date.txt'
	if os.path.isfile(date_file):
		ddate = readfile(date_file).decode('UTF')
		week1 = ''
		week2 = ''
		if ddate == '': msg = L('Read file error.')
		else:
			if len(text) <= 2:
				ltim = tuple(localtime())
				text = str(ltim[2])+' '+mmas2[ltim[1]-1]
				if ltim[0]/4.0 == int(ltim[0]/4): mtab = [31,29,31,30,31,30,31,31,30,31,30,31]
				else: mtab = [31,28,31,30,31,30,31,31,30,31,30,31]
				week1 = str(int(ltim[2]/7.0)+1*(int(ltim[2]/7.0)!=(ltim[2]/7.0))) + ' '+wday[ltim[6]]+' '+mmas2[ltim[1]-1]
				if ltim[2]+7 > mtab[ltim[1]-1]: week2 = lday[ltim[6]]+' '+wday[ltim[6]]+' '+mmas2[ltim[1]-1]
			or_text = text
			if text.count('.')==1: text = text.split('.')
			elif text.count(' ')==1: text = text.split(' ')
			else: text = [text]
			msg = ''
			ddate = ddate.split('\n')
			ltxt = len(text)
			for tmp in ddate:
				if tmp.lower().count(or_text.lower()): msg += '\n'+tmp
				elif tmp.lower().count(week1.lower()) and week1 != '': msg += '\n'+tmp
				elif tmp.lower().count(week2.lower()) and week2 != '': msg += '\n'+tmp
				else:
					try:
						ttmp = tmp.split(' ')[0].split('.')
						tday = [ttmp[0]]
						tday.append(dmas[int(ttmp[0])-1])
						tmonth = [ttmp[1]]
						tmonth.append(mmas1[int(ttmp[1])-1])
						tmonth.append(mmas2[int(ttmp[1])-1])
						tmonth.append(str(int(ttmp[1])))
						t = tday.index(text[0])
						t = tmonth.index(text[1])
						msg += '\n'+tmp
					except: pass
			if msg == '': msg = L('Holiday: %s not found.') % or_text
			else: msg = L('I know holidays: %s') % msg
	else: msg =L('Database doesn\'t exist.')
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, 'drink', to_drink, 2, L('Find holiday\ndrink [name_holiday/date]'))]
