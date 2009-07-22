#!/usr/bin/python
# -*- coding: utf -*-

'''	if text[:1] == '#':
		try:
			link = 'http://juick.com/'+str(int(text[1:]))
			body = urllib.urlopen(link).read()
			body = html_encode(body)
			print rss_del_html(body)
			msg = u'ok'
		except:
			msg = u'Не верный номер поста'
'''

def juick(type, jid, nick, text):
	if text[:9]== 'tag user ': juick_tag_user(type, jid, nick, text[9:])
	elif text[:8]== 'tag msg ': juick_tag_msg(type, jid, nick, text[8:])
	else: send_msg(type, jid, nick, u'Курим помощь по команде!')

def juick_tag_user(type, jid, nick, text):
	if len(text):
		link = 'http://juick.com/last?tag='+text.encode('utf-8').replace('\\x','%').replace(' ','%20')
		body = urllib.urlopen(link).read()
		body = html_encode(body)
		if body.count('<p>Tag not found</p>'):
			msg = u'Тег '+text+u' не найден'
		else:
			usr = body.split('<h2>Users</h2>')[1].split('<h2>Messages</h2>')[0].split('<a href')
			users = ''
			for us in usr[1:]:
				users += us[us.find('>')+1:us.find('<',us.find('>'))]+', '
			msg = u'Тег '+text+u' найден у '+users[:-2]
	else: msg = u'Какой тег найти?'
	send_msg(type, jid, nick, msg)

def juick_tag_msg(type, jid, nick, text):
	if len(text):
		try: mlen = int(text.split(' ')[1])
		except: mlen = 10
		try: mlim = int(text.split(' ')[2])
		except: mlim = 50
		text = text.split(' ')[0]
		link = 'http://juick.com/last?tag='+text.encode('utf-8').replace('\\x','%').replace(' ','%20')
		body = urllib.urlopen(link).read()
		body = html_encode(body)
		if body.count('<p>Tag not found</p>'):
			msg = u'Тег '+text+u' не найден'
		else:
			mes = body.split('<h2>Messages</h2>')[1].split('<h2>Tags</h2>')[0].split('<li id="')
			mesg = ''
			for us in mes[1:mlen+1]:
				mesg += '\n'+get_tag(us.split('</div>')[1],'a')+' '+get_tag(us.split('<big>')[1],'a')+' - '
				mm = rss_del_html(get_tag(us,'div'))
				if len(mm)<mlim: mesg += mm
				else: mesg += mm[:mlim]+'[...]'
				if us.split('</span>')[1].count('<a'): mesg += ' ('+get_tag(us,'span')+'|'+get_tag(us.split('</span>')[1],'a')+')'
				else: mesg += ' ('+get_tag(us,'span')+'|No replies)'
			msg = u'Тег '+text+u' найден в сообщениях:'+mesg
	else: msg = u'Какой тег найти?'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'juick', juick, 2, u'Миниблоги http://juick.com\njuick tag user <tag>\njuick tag msg <tag> [лимит_сообщенй [лимит_размера_сообщений]]')]
