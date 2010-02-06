#!/usr/bin/python
# -*- coding: utf-8 -*-

def bash_org_ru(type, jid, nick, text):
	try: url, splitter = 'http://bash.org.ru/quote/'+str(int(text)), '<div class="q">'
	except: url, splitter = 'http://bash.org.ru/random', '<hr class="iq">'
	body = html_encode(urllib.urlopen(url).read())
	if body.count('<div class="vote">') > 1 and url.count('quote'): msg = L('Quote not found!')
	else:
		body = body.split('<div class="vote">')[1].split(splitter)[0]
		msg = 'http://bash.org.ru/quote/'+str(get_tag(body, 'a'))+' ::: '
		msg = msg +rss_del_nn(rss_replace(body.split('</a> /',3)[3].replace('</div>', '\n').replace('<div>', '').replace('</a>\n', '')))
		if get_tag(msg,'a') == u'комикс' and msg.count('('+get_tag_full(msg,'a')+')'):
			msg = msg.replace('('+get_tag_full(msg,'a')+')',u'комикс: http://bash.org.ru'+get_subtag(msg,'a'))
	send_msg(type, jid, nick, msg)

def ibash_org_ru(type, jid, nick, text):
	try: url = 'http://ibash.org.ru/quote.php?id='+str(int(text))
	except: url = 'http://ibash.org.ru/random.php'
	body = html_encode(urllib.urlopen(url).read())
	msg = 'http://ibash.org.ru/quote.php?id='+replacer(body.split('<div class="quothead"><span>')[1].split('</a></span>')[0])[1:]
	if msg[-3:] == '???': msg = L('Quote not found!')
	else: msg += '\n'+rss_replace(body.split('<div class="quotbody">')[1].split('</div>')[0])
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, 'bash', bash_org_ru, 2, L('Quote from bash.org.ru\nbash [number]')),
		   (0, 'ibash', ibash_org_ru, 2, L('Quote from ibash.org.ru\nibash [number]'))]
