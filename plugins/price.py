#!/usr/bin/python
# -*- coding: utf -*-

# by ferym@jabbim.org.ru

def price(type, jid, nick, parameters):
	try:
		if parameters.count('http://'):
			send_msg(type, jid, nick, L('site input format is domain.tld'))
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
			send_msg(type, jid, nick, L('Estimated value %s is %s') % (parameters.strip(), message))
		else:
			send_msg(type, jid, nick, L('What site be evaluated?'))
	except:
		send_msg(type, jid, nick, L('I can\'t process your request.'))

# by dissy@isida-bot.com

def bizinfo(type, jid, nick, text):
	try:
		if text.count('http://'):
			msg = L('site input format is domain.tld')
		elif len(text):
			text = text.split('.')[-2].lower()+'.'+text.split('.')[-1].lower()
			req = 'http://bizinformation.org/ru/www.'+text
			r = urllib2.urlopen(req)
			body = unicode(r.read().strip(),'utf-8')
			if body.count('How Much'): msg = L('site input format is domain.tld')
			else: msg = L('Estimated value %s is %s') % (text.strip(), get_tag(body,'span'))
		else: msg = L('What site be evaluated?')
	except: msg = L('I can\'t process your request.')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'price', price, 2, L('Show estimated value of domain | Author: ferym')),
           (3, 'bizinfo', bizinfo, 2, L('Show estimated value of domain | Author: Disabler'))]
