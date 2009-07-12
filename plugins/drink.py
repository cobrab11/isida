#!/usr/bin/python
# -*- coding: utf -*-

def to_drink(type, jid, nick, text):
	dmas = [u'первое',u'второе',u'третье',u'червертое',u'пятое',u'шестое',u'седьмое',u'восьмое',u'девятое',u'десятое',
		u'одинадцтое',u'двенадцатое',u'тринадцатое',u'четырнадцатое',u'пятнадцатое',u'шестнадцатое',
		u'семнадцатое',u'восемнадцатое',u'девятнадцатое',u'двадцатое',u'двадцатьпервое',u'двадцатьвторое',
		u'двадцатьтретье',u'двадцатьчетвертое',u'двадцатьпятое',u'двадцатьшестое',u'двадцатьседьмое',
		u'двадцатьвосьмое',u'двадцатьдевятое',u'тридцатое',u'дридцатьпервое']
	mmas1 = [u'январь',u'февраль',u'март',u'апрель',u'май',u'июнь',u'июль',u'август',
		u'сентябрь',u'октябрь',u'ноябрь',u'декабрь']
	mmas2 = [u'января',u'февраля',u'марта',u'апреля',u'мая',u'июня',u'июля',u'августа',
		u'сентября',u'октября',u'ноября',u'декабря']
	date_file = 'plugins/date.txt'
	if os.path.isfile(date_file):
		ddate = readfile(date_file).decode('UTF')
		if ddate == '':
			msg = u'Ошибка чтения файла!'
		else:
			if len(text) <= 2:
				ltim = tuple(localtime())
				text = str(ltim[2])+' '+mmas2[ltim[1]-1]
				if not ddate.count(str(ltim[2])+'.'+str(ltim[1])) and ltim[6] == 6:
					if ltim[0]/4.0 == int(ltim[0]/4):
						mtab = [31,29,31,30,31,30,31,31,30,31,30,31]
					else:
						mtab = [31,28,31,30,31,30,31,31,30,31,30,31]
					text = str(int(ltim[2]/7.0)+1*(int(ltim[2]/7.0)!=(ltim[2]/7.0))) + u' воскресенье '+mmas2[ltim[1]-1]
					if ltim[2]+7 > mtab[ltim[1]]:
						week = u'последнее воскресенье '+mmas2[ltim[1]-1]
					else:
						week = u''
			or_text = text
			if text.count('.')==1:
				text = text.split('.')
			elif text.count(' ')==1:
				text = text.split(' ')
			else:
				text = [text]
			msg = ''
			ddate = ddate.split('\n')
			ltxt = len(text)
			for tmp in ddate:
				if len(text)!=2:
					if tmp.lower().count(text[0].lower()):
						msg += '\n'+tmp
					if tmp.lower().count(week.lower()) and week != '':
						msg += '\n'+tmp
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
					except:
						t = None

			if msg == '':
				msg = u'Повод '+or_text+u' не найден!'
			else:
				msg = u'Я знаю поводы выпить:'+msg
	else:
		msg =u'К сожалению база отсутствует.'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'drink', to_drink, 2)]
