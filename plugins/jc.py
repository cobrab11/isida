#!/usr/bin/env python
# -*- coding: utf-8 -*-

def jc(type, jid, nick, text):
	if not len(text): text = getName(jid)
	try:	
		url = u'http://jc.jabber.ru/search.html?%s'.encode("utf-8") % (urllib.urlencode({'search': text.encode("utf-8")}))
		user_agent='Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'
		req = urllib2.Request(url)
		req.add_header('User-Agent',user_agent)
		body = urllib2.urlopen(req).read()
		body = html_encode(body)
		body = get_tag(body,'ol')
		if body.count('<li>'):
			body = body.split('<li>')[1:]
			msg, cnt = L('Found:'), 1
			for tmp in body:
				msg += '\n'+str(cnt)+'. '+get_tag(tmp,'font')+' ['+tmp.split(u'комнате: ')[1].split(u'&nbsp;')[0]+u'] • '
				msg += tmp.split('<br>')[1][1:].replace('<b>', u'«').replace('</b>', u'»')+u' • рейтинг: '+tmp.split(u'рейтинге: ')[1].split(u'</font>')[0]
				cnt += 1
			if type=='groupchat' and len(msg)>600:
				send_msg('chat', jid, nick, msg)
				msg = L('Send for you in private')
		else: msg = L('Not found.')
	except: msg = L('Error!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'jc', jc, 2, L('Show information about conference from jc.jabber.ru.\njc [address]'))]
