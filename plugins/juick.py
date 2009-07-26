#!/usr/bin/python
# -*- coding: utf -*-

def juick(type, jid, nick, text):
	if text[:9]== 'tag user ': juick_tag_user(type, jid, nick, text[9:])
	elif text[:8]== 'tag msg ': juick_tag_msg(type, jid, nick, text[8:])
	elif text[:4]== 'msg ': juick_msg(type, jid, nick, text[4:])
	elif text[:5]== 'user ': juick_user(type, jid, nick, text[5:])
	elif text[:5]== 'info ': juick_user_info(type, jid, nick, text[5:])
	else: send_msg(type, jid, nick, u'Курим помощь по команде!')

def juick_user_info(type, jid, nick, text):
	if len(text):
		try: mlen = int(text.split(' ')[1])
		except: mlen = 3
		try: mlim = int(text.split(' ')[2])
		except: mlim = 50
		text = text.split(' ')[0]
		link = 'http://juick.com/'+text.encode('utf-8').replace('\\x','%').replace(' ','%20')+'/friends'
		body = urllib.urlopen(link).read()
		body = html_encode(body)
		if body.count('<title>404 Not Found</title>'):
			msg = u'Пользователь '+text+u' не найден'
		else:
			msg = get_tag(body,'h1')+' - http://juick.com'+get_subtag(body.split('pagetabs')[1].split('</li>')[0],'href')
			tb = body.split('<div id="content">')[1].split('</div>')[0]
			try:
				if len(tb)>=20 and tb.count('I read'):
					msg += '\n'+get_tag(tb,'h2')+' - '
					for tmp in tb.split('<p>')[1].split('<a href="')[1:]:
						msg += tmp[tmp.find('>')+1:tmp.find('<',tmp.find('>'))]+', '
					msg = msg[:-2]
				else: msg += '\nNo readers'
			except:
				msg += '\nNo readers'
			try:
				if len(tb)>=20 and tb.count('My read'):			
					tb = body.split('</p>')[1]
					msg += '\n'+get_tag(tb,'h2')+' - '
					for tmp in tb.split('<p>')[1].split('<a href="')[1:]:
						msg += tmp[tmp.find('>')+1:tmp.find('<',tmp.find('>'))]+', '
					msg = msg[:-2]
				else: msg += '\nNo readers'
			except:
				msg += '\nNo readers'
			try:
				tb = body.split('<div id="lcol">')[1].split('<div>')[0]
				if len(tb)>=20 and tb.count('</a></p>'):
					tb.split('</a></p>')[0]
#					msg += '\n'+get_tag(tb,'h2')+':'
					for ttb in tb.split('<br/>')[1:]:
						msg += '\n'+get_tag(ttb,'a')+' - '+get_subtag(ttb,'href')
				else: msg += '\nNo info'
			except:
				msg += '\nNo info'
			try:
				if body.count('<h2>Tags</h2>'):
					tb = body.split('<h2>Tags</h2>')[1].split('</p>')[0]
					msg += u'\nTags: '
					for ttb in tb.split('<a href')[1:]:
						msg += ttb[ttb.find('>')+1:ttb.find('<',ttb.find('>'))]+', '
					msg = msg[:-2]
				else: msg += '\nNo tags'
			except:
				msg += '\nNo tags'
	else: msg = u'Кто нужен то?'
	send_msg(type, jid, nick, msg)

def juick_user(type, jid, nick, text):
	if len(text):
		try: mlen = int(text.split(' ')[1])
		except: mlen = 3
		try: mlim = int(text.split(' ')[2])
		except: mlim = 50
		text = text.split(' ')[0]
		link = 'http://juick.com/'+text.encode('utf-8').replace('\\x','%').replace(' ','%20')
		body = urllib.urlopen(link).read()
		body = html_encode(body)
		if body.count('<title>404 Not Found</title>'):
			msg = u'Пользователь '+text+u' не найден'
		else:
			msg = get_tag(body,'h1')+' - http://juick.com'+get_subtag(body.split('pagetabs')[1].split('</li>')[0],'href')
			mes = body.split('<li id="')
			mesg = ''
			for us in mes[1:mlen+1]:
				mesg += '\n'+get_tag(us.split('<small>')[1],'a')+' - '
				mm = rss_del_html(get_tag(us,'div'))
				if len(mm)<mlim: mesg += mm
				else: mesg += mm[:mlim]+'[...]'
				if us.split('</span>')[1].count('<a'): mesg += ' ('+get_tag(us,'span')+'|'+get_tag(us.split('</span>')[1],'a')+')'
				else: mesg += ' ('+get_tag(us,'span')+'|No replies)'
			msg += mesg
	else: msg = u'Кто нужен то?'
	send_msg(type, jid, nick, msg)

def juick_msg(type, jid, nick, text):
	if len(text):
		try:
			text = text.replace('#','')
			if text.count('/'):
				link = 'http://juick.com/'+text.split('/')[0]
				post = int(text.split('/')[1])
			else: 
				post = 0
				link = 'http://juick.com/'+text.split(' ')[0]
			try: repl_limit = int(text.split(' ')[1])
			except: repl_limit = 3
			body = urllib.urlopen(link).read()
			body = html_encode(body.replace('<div><a href','<div><a '))
			if body.count('<title>404 Not Found</title>'):
				msg = u'Пост #'+text+u' не найден'
			else:
				nname = get_tag(body,'h1')
				msg = 'http://juick.com/'+nname[nname.find('(')+1:nname.find(')')]+'/'+text.split(' ')[0]+'\n'+nname+' - '+get_tag(body.split('<p>')[1],'div')
			repl = get_tag(body.split('<p>')[1],'h2')
			if repl.lower().count('('):
				hm_repl = int(repl[repl.find('(')+1:repl.find(')')])
				msg += u' (Ответов: '+str(hm_repl)+')'
			else:
				hm_repl = 0
				msg += u' (Нет ответов)'
			frm = get_tag(body.split('<p>')[1],'small')
			msg += frm[frm.find(' '):]
			cnt = 1
			if hm_repl:
				if not post:
					for rp in body.split('<li id="')[1:repl_limit+1]:
						print cnt, '--------------\n',rp
						msg += '\n'+text.split(' ')[0]+'/'+str(cnt)+' '+get_tag(rp.split('by')[1],'a')+': '+get_tag(rp,'div')
						cnt += 1
				else:
					msg += '\n'+text+' '+get_tag(body.split('<li id="')[post],'div')
			msg = rss_del_html(msg.replace('<a href="http','<a>http').replace('" rel',' <'))
		except:
			msg = u'Неверный номер поста'
	else: msg = u'Какой пост найти?'
	send_msg(type, jid, nick, msg)

def juick_tag_user(type, jid, nick, text):
	if len(text):
		try: mlen = int(text.split(' ')[1])
		except: mlen = 5
		if mlen > 20: mlen = 20
		link = 'http://juick.com/last?tag='+text.split(' ')[0].encode('utf-8').replace('\\x','%').replace(' ','%20')
		body = urllib.urlopen(link).read()
		body = html_encode(body)
		if body.count('<p>Tag not found</p>'):
			msg = u'Тег '+text+u' не найден'
		else:
			usr = body.split('<h2>Users</h2>')[1].split('<h2>Messages</h2>')[0].split('<a href')
			users = ''
			for us in usr[1:mlen+1]:
				uus = us[us.find('>')+1:us.find('<',us.find('>'))]
				users += '\n'+ uus + ' - http://juick.com/'+uus[1:]
			msg = u'Тег '+text+u' найден у '+users
	else: msg = u'Какой тег найти?'
	send_msg(type, jid, nick, msg)

def juick_tag_msg(type, jid, nick, text):
	if len(text):
		try: mlen = int(text.split(' ')[1])
		except: mlen = 3
		try: mlim = int(text.split(' ')[2])
		except: mlim = 120
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
				mesg += '\nhttp://juick.com/'+get_tag(us.split('<big>')[1],'a')[1:]+'/'+get_tag(us.split('</div>')[1],'a')[1:]+' - '
				mm = rss_del_html(get_tag(us,'div'))
				if len(mm)<mlim: mesg += mm
				else: mesg += mm[:mlim]+'[...]'
				if us.split('</span>')[1].count('<a'): mesg += ' ('+get_tag(us,'span')+'|'+get_tag(us.split('</span>')[1],'a')+')'
				else: mesg += ' ('+get_tag(us,'span')+'|No replies)'
			msg = u'Тег '+text+u' найден в сообщениях:'+mesg
	else: msg = u'Какой тег найти?'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'juick', juick, 2, u'Миниблоги http://juick.com\njuick tag user <tag>[ количество_пользователей] - пользователи, использующие теги\njuick tag msg <tag>[ лимит_сообщенй [лимит_размера_сообщений]] - сообщения с заданными тегами\njuick msg <номер_поста>[ количество] - пост+количество ответов\njuick msg <номер_поста/номер_ответа> - пост+ответ на пост\njuick user <user> [лимит_сообщенй [лимит_размера_сообщений]] - последние сообщения пользователя\njuick info <user> - информация о пользователе')]
