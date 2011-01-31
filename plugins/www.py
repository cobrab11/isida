#!/usr/bin/python
# -*- coding: utf-8 -*-

last_url_watch = ''

def netheader(type, jid, nick, text):
	if text:
		try:
			regex = text.split('\n')[0].replace('*','*?')
			text = text.split('\n')[1]
		except: regex = None
		if '://' not in text[:10]: text = 'http://%s' % text
		req = text.encode("utf-8")
		body, result = get_opener(req)
		if result: body = text + '\n' + str(body.headers)
		if regex:
			try:
				mt = re.findall(regex, body, re.S)
				if mt != []: body = ''.join(mt[0])
				else: body = L('RegExp not found!')
			except: body = L('Error in RegExp!')
	else: body = L('What?')
	send_msg(type, jid, nick, body)

def netwww(type, jid, nick, text):
	try:
		regex = text.split('\n')[0].replace('*','*?')
		text = text.split('\n')[1]
	except: regex = None
	if '://' not in text[:10]: text = 'http://%s' % text
	req = text.encode('utf-8')
	msg, result = get_opener(req)
	if result:
		msg = str(msg.info())
		mt = re.findall('Content-Length.*?([0-9]+)', msg, re.S)
		msg = None
		if mt != []:
			try:
				c_size = int(''.join(mt[0]))
				if c_size > GT('size_overflow'): msg = L('Site size limit overflow! Size - %skb, allowed - %skb') % (str(c_size/1024),str(GT('size_overflow')/1024))
			except: c_size = GT('size_overflow')
		else: c_size = GT('size_overflow')
		if not msg:
			page = remove_sub_space(html_encode(load_page(req)))
			if regex:
				try:
					mt = re.findall(regex, page, re.S+re.U)
					if mt != []: msg = unhtml_hard(''.join(mt[0]))
					else: msg = L('RegExp not found!')
				except: msg = L('Error in RegExp!')
			else:
				msg = urllib.unquote(unhtml_hard(page).encode('utf8')).decode('utf8')
				if '<title' in page: msg = '%s\n%s' % (get_tag(page,'title'), msg)
	send_msg(type, jid, nick, msg[:msg_limit])

def parse_url_in_message(room,jid,nick,type,text):
	global last_url_watch
	if type != 'groupchat' or text == 'None' or nick == '' or getRoom(jid) == getRoom(selfjid): return
	if not get_config(getRoom(room),'url_title'): return
	if get_level(room,nick)[0] < 4: return
	try:
		link = re.findall(r'(http[s]?://.*)',text)[0].split(' ')[0]
		if link and last_url_watch != link and not link.count(pasteurl):
			last_url_watch = link
			req = urllib2.Request(link.encode('utf-8'))
			req.add_header('User-Agent',GT('user_agent'))
			page = remove_sub_space(html_encode(load_page(req)))
			if page.count('<title>'): tag = 'title'
			elif page.count('<TITLE>'): tag = 'TITLE'
			else: return
			text = get_tag(page,tag).replace('\n',' ').replace('\r',' ').replace('\t',' ')
			while text.count('  '): text = text.replace('  ',' ')
			if text: send_msg(type, room, '', L('Title: %s') % rss_del_html(rss_replace(text)))
	except: pass

global execute

message_act_control = [parse_url_in_message]

execute = [(3, 'www', netwww, 2, L('Show web page.\nwww regexp\n[http://]url - page after regexp\nwww [http://]url - without html tags')),
		   (3, 'header',netheader,2, L('Show net header'))]
