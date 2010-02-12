#!/usr/bin/python
# -*- coding: utf-8 -*-

def currency_converter(type, jid, nick, text):
	if text == 'list':
		#url = 'http://conv.rbc.ru/convert.shtml?mode=calc&source=cb.0&tid_from=EUR&commission=1&tid_to=BASE&summa=100&day=13&mon=10&year=2009'
		#body = html_encode(urllib.urlopen(url).read())
		#msg = u'Допустимые значения:\n'
		#body = body.split('<TD><SELECT class=n name=tid_from>')[1].split('</SELECT></TD>')[0].replace('\t', '').split('<')
		#for i in range(1, len(body)): msg += body[i].split('\"')[1]+' '
		msg = L('Aviable values:\n%s') % 'ATS AUD BASE BEF BYR CAD CHF CNY DEM DKK EEK EGP ESP EUR FIM FRF GBP GRD IEP ISK ITL JPY KGS KWD KZT LTL NLG NOK PTE RUR SDR SEK SGD TRL TRY UAH USD XDR YUN'
	elif text.count(' '):
		if text.lower().count('rur'): text = text.lower().replace('rur', 'base')
		try:
			text, date = text.split(' '), tuple(localtime())[:3]
			url = 'http://conv.rbc.ru/convert.shtml?mode=calc&source=cb.0&tid_from='+text[0].upper()+'&commission=1&tid_to='+text[1].upper()+'&summa='+text[2].upper()+'&day='+str(date[2])+'&month='+str(date[1])+'&year='+str(date[0])
			body = html_encode(urllib.urlopen(url).read())
			body = body.split('<TABLE height=120 cellSpacing=1 cellPadding=4 width=300 border=0>')[1].split('</TR></TBODY></TABLE></TD>')[0]
			msg = replacer(body).replace(':\n', ': ')
		except: msg = L('Error in parameters. Read the help about command.')
	else: msg = L('Error in parameters. Read the help about command.')
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, 'convert', currency_converter, 2, L('Currency converter\nconvert from to count\nconvert list'))]
