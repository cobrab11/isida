#!/usr/bin/python
# -*- coding: utf-8 -*-

dumpz_var = {'sh':'bash', 'bash':'bash', 'c':'c', 'h':'c', 'html':'html', 'htm':'html', 'python':'python', 'py':'python', 'php':'php', 'css':'css', 'sql':'sql', 'cpp':'cpp', 'hpp':'cpp'}

def dumpz(type, jid, nick, text):
	try:
		p = text.split(' ',1)
		if p[0].lower() in dumpz_var.keys():
			highlighting = dumpz_var[p[0].lower()]
			code = p[1]
		else:
			highlighting = 'text'
			code = text
		values = {'lexer': highlighting, 'code': code.encode('utf-8'),}
		data = urllib.urlencode(values)
		req = urllib2.Request('http://dumpz.org/' ,data,{'Content-type':'application/x-www-form-urlencoded'})
		res = urllib2.urlopen(req)
		link = res.url
		msg = L('Posting by URL: %s') % link
	except:
		msg = L('Unexpected error')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'dumpz', dumpz, 2, L('Posting text&code on dedicated server for easy sharing.\ndumpz text - posting plain text,\ndumpz [sh|c|html|py|php|css|sql|cpp] - posting text with highlighting'))]

