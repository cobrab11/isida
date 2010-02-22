#!/usr/bin/python
# -*- coding: utf-8 -*-

user_agent = 'Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'
size_overflow = 262144	# лимит страницы в байтах для команды просмотра.

def netheader(type, jid, nick, text):
	if len(text):
		if not text.count('://'): text = 'http://'+text
		req = urllib2.Request(text)
		req.add_header('User-Agent',user_agent)
		try: body = str(urllib2.urlopen(req).headers)
		except: body = L('I can\'t do it')
	else: body = L('What?')
	send_msg(type, jid, nick, body)	

def netwww(type, jid, nick, text):
	try:
		regex = text.split('\n')[0].replace('*','*?')
		text = text.split('\n')[1]
	except: regex = None
	if not text.count('://'): text = 'http://'+text
	req = urllib2.Request(text)
	req.add_header('User-Agent',user_agent)
	try: body = str(urllib2.urlopen(req).headers)
	except: body = L('I can\'t do it')
	mt = re.findall('Content-Length.*?([0-9]+)', body, re.S)
	msg = None
	if mt != []:
		try:
			c_size = int(''.join(mt[0]))
			if c_size > size_overflow: msg = L('Site size limit overflow! Size - %skb, allowed - %skb') % (str(c_size/1024),str(size_overflow/1024))
		except: msg = L('Unable detect size!')
	else: msg = L('Unable detect size!')
	if not msg:
		try:
			page = html_encode(urllib2.urlopen(req).read())
			if regex:
				try:
					mt = re.findall(regex, page, re.S)
					if mt != []: msg = unhtml(''.join(mt[0]))
					else: msg = L('RegExp not found!')
				except: msg = L('Error in RegExp!')
			else: msg = get_tag(page,'title')+'\n'+unhtml(page)
		except Exception, SM: msg = str(SM)
	send_msg(type, jid, nick, msg[:msg_limit])

global execute

execute = [(0, 'www', netwww, 2, L('Show web page.\nwww regexp\n[http://]url - page after regexp\nwww [http://]url - without html tags')),
		   (0, 'header',netheader,2, L('Show net header'))]
