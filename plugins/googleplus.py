#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Vit@liy

def gcalc(type, jid, nick, text):
	if not text.strip(): msg = L('What?')
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

def define(type, jid, nick, text):
	text = text.strip()
	target = ''
	if not text: msg = L('What?')
	else:
		if re.search('\A\d+?(-\d+?)? ', text): target, text = text.split(' ', 1)
		query=urllib.urlencode({'q':'define:'+text.encode('utf-8')})
		start='<h2 class=r style="font-size:138%"><b>'
		end='</b>'
		google=httplib.HTTPConnection("www.google.ru")
		google.request("GET","/search?"+query)
		search=google.getresponse()
		data=search.read()
		result = re.findall('<li>(.+?)<font color=#008000>(.+?)</font></a><p>', data)

		if not result: msg = L('Define not found')
		else:
			if target:
				try: n1 = n2 = int(target)
				except: n1, n2 = map(int, target.split('-'))
				msg = ''
				if 0 < n1 <= n2 <= len(result): 
					for k in xrange(n1-1,n2): msg += result[k][0] + '\nhttp://' + result[k][1] + '\n\n'
				else: msg = L('Define not found')
			else:
				result = random.choice(result)
				msg = result[0] + '\nhttp://' + result[1]
			msg = re.sub(r'<[^<>]+>', ' ', msg).strip()
			msg = rss_replace(msg.decode('cp1251'))
	send_msg(type, jid, nick, msg)


def define_message(room,jid,nick,type,text):
	if get_config(room,'parse_define'):
		access_mode, jid = get_level(room,nick)
		tmppos = arr_semi_find(confbase, room)
		nowname = getResourse(confbase[tmppos])
		what = re.search(u'^что такое (.+?)\?$', text.strip(), re.I+re.U)
		if what:
			text = 'define 1 ' + what.group(1)
			com_parser(access_mode, nowname, type, room, nick, text, jid)


global execute, message_control

message_control = [define_message]

execute = [(3, 'gcalc', gcalc, 2, L('Google Calculator. Author: Vit@liy')),
	(3, 'define', define, 2, L('Definition for a word or phrase.\ndefine word - random define of word or phrase\ndefine N word - N-th define of word or phrase\ndefine a-b word - from a to b defines of word or phrase'))]
