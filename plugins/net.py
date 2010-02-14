#!/usr/bin/python
# -*- coding: utf -*-

def get_tld(type, jid, nick, text):
	if len(text) >= 2:
		tld = readfile('tld/tld.list').decode('utf-8')
		tld = tld.split('\n')
		msg = L('Not found!')
		for tl in tld:
			if tl.split('\t')[0].lower()==text.lower():
				msg = '.'+tl.replace('\t',' - ',1).replace('\t','\n')
				break
	else: msg = L('What do you want to find?')
	send_msg(type, jid, nick, msg)

def get_dns(type, jid, nick, text):
	is_ip = None
	if text.count('.') == 3:
		is_ip = True
		for ii in text:
			if not nmbrs.count(ii):
				is_ip = None
				break
	if is_ip:
		try: msg = socket.gethostbyaddr(text)[0]
		except: msg = L('I can\'t resolve it')
	else:
		try:
			ans = socket.gethostbyname_ex(text)[2]
			msg = text+' - '
			for an in ans: msg += an + ' | '
			msg = msg[:-2]
		except: msg = L('I can\'t resolve it')
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, 'dns', get_dns, 2, L('DNS resolver.')),
	 (0, 'tld', get_tld, 2, L('Search domain zones TLD.'))]
