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
	reg_title = '<div class="quothead">.*?<b>#(.*?)</b>'
	reg_body = '<div class="quotbody">(.*?)</div>'
	url_id = 'http://ibash.org.ru/quote.php?id='
	try: url = url_id+str(int(text))
	except: url = 'http://ibash.org.ru/random.php'
	body = html_encode(urllib.urlopen(url).read())
	msg = url_id + re.findall(reg_title, body, re.S)[0]
	if msg[-3:] == '???': msg = L('Quote not found!')
	else: msg += '\n'+rss_replace(re.findall(reg_body, body, re.S)[0])
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'bash', bash_org_ru, 2, L('Quote from bash.org.ru\nbash [number]')),
		   (3, 'ibash', ibash_org_ru, 2, L('Quote from ibash.org.ru\nibash [number]'))]
