#!/usr/bin/python
# -*- coding: utf -*-

JUICK_JID = 'juick@juick.com'

NS_JUICK = 'http://juick.com/query'
NS_JUICK_MSG = '%s#messages' % NS_JUICK

def juick(type, jid, nick, text):
	topt = text.split(' ',1)
	topt[0] = topt[0].lower()
	if topt[0] == 'msg': juick_msg(type, jid, nick, topt[1])
	else:
		try: tmpt = re.findall('(#?[0-9]+\/?[0-9]+)',text)[0]
		except: tmpt = ''
		if tmpt == text: juick_msg(type, jid, nick, text)
		else: send_msg(type, jid, nick, L('Smoke help about command!'))

def juick_msg(type, jid, nick, text):
	global iq_request
	if not len(text) or len(text) == text.count(' '):
		send_msg(type, jid, nick, L('What message do you want to find?'))
		return
	j_mid,j_rid = re.findall('#?([0-9]+)\/?([0-9]+)?',text)[0]
	if len(j_rid):
		if int(j_rid) == 0: raise SyntaxError
		else: j_rid = str(int(j_rid))
	j_mid = str(int(j_mid))
	try: j_replies = int(text.split()[1])
	except: j_replies = GT('juick_msg_answers_default')
	iqid = get_id()
	j_items = {'xmlns': NS_JUICK_MSG,
			   'mid':j_mid}
	#if len(j_rid): j_items['rid'] = '*'
	#if j_replies > 0: j_items['rid'] = '*'
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':JUICK_JID}, payload = [Node('query', j_items,[])])
	iq_request[iqid]=(time.time(),juick_msg_async,[type, jid, nick, (j_mid,j_rid,j_replies)])
	sender(i)

def juick_msg_async(type, jid, nick, (j_mid,j_rid,j_replies), is_answ):
	isa = is_answ[1][0]
	print isa
	j_type = get_tag_item(isa,'iq','type')
	if j_type == 'error':
		j_error_code = get_tag_item(isa,'error','code')
		if j_error_code == '404': msg = L('Message #%s is not found!') % j_mid
		elif j_error_code == '403': msg = L('I can\'t show message #%s!') % j_mid
		else: msg = L('Unknown error while message #%s parsing!') % j_mid
	elif j_type == 'result':
		j_item 		= rss_replace(get_tag_full(isa,'juick'))
		ja_body 	= rss_replace(get_tag(j_item,'body'))
		j_item 		= j_item.replace(ja_body,'')
		ja_ts 		= get_tag_item(j_item,'juick','ts')
		ja_uname 	= rss_replace(get_tag_item(j_item,'juick','uname'))
		ja_replies 	= rss_replace(get_tag_item(j_item,'juick','replies'))
		ja_attach 	= rss_replace(get_tag_item(j_item,'juick','attach'))
		ja_tags 	= []
		while j_item.count('<tag') and j_item.count('</tag>'):
			tmp_tag = get_tag_full(j_item,'tag')
			j_item = j_item.replace(tmp_tag,'')
			ja_tags.append(rss_replace(get_tag(tmp_tag,'tag')))
		msg = '@%s:' % ja_uname
		if len(ja_tags): msg = '%s *%s' % (msg,' *'.join(ja_tags))
		if ja_attach in ['jpg', '3gp', 'wmv', 'mov','mp4']:
			if ja_attach in ['3gp', 'wmv', 'mov','mp4']: ja_url = 'http://i.juick.com/video/'
			elif ja_attach in ['jpg']: ja_url = 'http://i.juick.com/p/'
			msg = '%s - %s%s.%s' % (msg,ja_url,j_mid,ja_attach)
		msg = '%s\n%s\n#%s, %s' % (msg,ja_body,j_mid,ja_ts)
		if len(ja_replies): msg = '%s; %s %s' % (msg,L('Replies:'),ja_replies)
	else: msg = L('Unknown server ansver!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'juick', juick, 2, L('Miniblogs http://juick.com\njuick [msg][#]post - show post'))]
