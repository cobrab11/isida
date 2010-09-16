#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Vit@liy

def gcalc(type, jid, nick, text):
	if not len(text) or len(text) == text.count(' '): msg = L('What?')
	else:
		query=urllib.urlencode({'q':text.encode('utf-8')})
		start='<h2 class=r style="font-size:138%"><b>'
		end='</b>'
		google=httplib.HTTPConnection("www.google.ru")
		google.request("GET","/search?"+query)
		search=google.getresponse()
		data=search.read()

		if data.find(start)==-1: msg = L('Google Calculator results not found')
		else:
			begin=data.index(start)
			result=data[begin+len(start):begin+data[begin:].index(end)]
			result = result.replace("<font size=-2> </font>",",").replace(" &#215; 10<sup>","E").replace("</sup>","").replace("\xa0",",").replace('<sup>','^')
			msg = result.decode('cp1251')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'gcalc', gcalc, 2, L('Google Calculator. Author: Vit@liy'))]
