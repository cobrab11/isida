#!/usr/bin/python
# -*- coding: utf -*-

def netwww(type, jid, nick, text):
	try:
		regex = text.split('\n')[0]
		text = text.split('\n')[1]
	except: regex = None

	text = text.encode('utf-8').replace('\\x','%').replace(' ','%20')
	if text[:7] !='http://': text = 'http://'+text
	f = urllib.urlopen(text)
	page = f.read()
	f.close()

	page = html_encode(page)
#	page = rss_replace(page)
	if regex:
		mt = re.findall(r''+regex, page, re.S)
		for a in mt:
			print a[:50]
		if mt != []:
			mt = tuple(mt[0])
			msg = ''
			for tmp in mt:
				msg += tmp
		else:
			msg = u'RegExp не найден!'
	else:
		msg = get_tag(page,'title')+'\n'
		msg += unhtml(page)
	send_msg(type, jid, nick, msg[:msg_limit])

global execute

execute = [(1, u'www', netwww, 2, u'Показывает содержимое веб страницы.\nwww regexp\n[http://]url - страница, обработанная regexp\nwww [http://]url - страница с убранными html тегами')]
