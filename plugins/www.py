#!/usr/bin/python
# -*- coding: utf -*-

user_agent='Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'

def netheader(type, jid, nick, text):
	if len(text):
		if text[:7] !='http://': text = 'http://'+text
		req = urllib2.Request(text)
		req.add_header('User-Agent',user_agent)
		try: body = str(urllib2.urlopen(req).headers)
		except: body = u'Что-то не получается!'
	else: body = u'Что посмотреть?'
	send_msg(type, jid, nick, body)	

def netwww(type, jid, nick, text):
	try:
		regex = text.split('\n')[0]
		text = text.split('\n')[1]
	except: regex = None

	text = text.encode('utf-8').replace('\\x','%').replace(' ','%20')
	if text[:7] !='http://': text = 'http://'+text

	req = urllib2.Request(text)
	req.add_header('User-Agent',user_agent)
	try: page = urllib2.urlopen(req).read()
	except: page = u'forbidden'

	page = html_encode(page)
#	page = rss_replace(page)
	if regex:
		mt = re.findall(r''+regex, page, re.S)
#		for a in mt:
#			print a[:50]
		if mt != []:
			mt = tuple(mt[0])
			msg = ''
			for tmp in mt: msg += tmp
		else: msg = u'RegExp не найден!'
	else:
		msg = get_tag(page,'title')+'\n'
		msg += unhtml(page)
	send_msg(type, jid, nick, msg[:msg_limit])

global execute

execute = [(0, u'www', netwww, 2, u'Показывает содержимое веб страницы.\nwww regexp\n[http://]url - страница, обработанная regexp\nwww [http://]url - страница с убранными html тегами'),
		   (0, u'header',netheader,2, u'Показывает заголовок файла')]
