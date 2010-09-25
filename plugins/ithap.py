#!/usr/bin/python
# -*- coding: utf-8 -*-

def ithap(type, jid, nick, text):
	if text.strip(): url = 'http://ithappens.ru/story/'+text.strip()
	else: url = 'http://ithappens.ru/random/'
	try:
		body = html_encode(urllib.urlopen(url).read())
		message = re.search('<p class="text">(.+?)</p>', body).group()
		msg = unhtml(message)
	except:
		msg = L('Quote not found!')
	send_msg(type, jid, nick, msg)	

global execute

execute = [(3, 'ithap', ithap, 2, L('Quote from ithappens.ru\nithap [number]'))]
