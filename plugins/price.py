#!/usr/bin/python
# -*- coding: utf -*-

# by ferym@jabbim.org.ru

def price(type, jid, nick, parameters):
	try:
		if parameters.count('http://'):
			send_msg(type, jid, nick, u'формат ввода сайта domain.tld')
			return
		if len(parameters):
			parameters = parameters.split('.')[-2].lower()+'.'+parameters.split('.')[-1].lower()
			req = 'http://www.webvaluer.org/ru/www.'+parameters
			r = urllib2.urlopen(req)
			target = r.read()
			od = re.search('<span style=\"color:green; font-weight:bold;\">',target)
			message = target[od.end():]
			message = message[:re.search('</span></h1>',message).start()]
			message = message.replace(',','')
			message = unicode(message.strip(),'utf-8')
			try: pos = message.find(re.findall(r'[0-9]',message)[0])
			except: pos = None
			if pos:
				if pos >= 2: message = message[pos:]+' '+message[:pos]
			send_msg(type, jid, nick, u'Оценочная стоимость домена '+parameters.strip()+u' составляет - '+message)
		else:
			send_msg(type, jid, nick, u'какой сайт оценивать?')
	except:
		send_msg(type, jid, nick, u'Не получилось обработать запрос')

		# by dissy@isida-bot.com

def bizinfo(type, jid, nick, text):
	try:
		if text.count('http://'):
			msg = u'формат ввода сайта domain.tld'
		elif len(text):
			text = text.split('.')[-2].lower()+'.'+text.split('.')[-1].lower()
			req = 'http://bizinformation.org/ru/www.'+text
			r = urllib2.urlopen(req)
			body = unicode(r.read().strip(),'utf-8')
			if body.count('How Much'): msg = u'Ошибка формата адреса!'
			else: msg = u'Оценочная стоимость домена '+text.strip()+u' составляет - '+get_tag(body,'span')
		else: msg = u'какой сайт оценивать?'
	except: msg = u'Не получилось обработать запрос'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'price', price, 2, u'Показывает ориентировочную оценочную стоимость домена | Author: ferym'),
           (0, u'bizinfo', bizinfo, 2, u'Показывает ориентировочную оценочную стоимость домена | Author: Disabler')]
