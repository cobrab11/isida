#!/usr/bin/python
# -*- coding: utf -*-

bmn_last_res = {}

def dec(data):
	b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
	enc = ''
	for i in range(0, len(data)/4):
		h1 = b64.index(data[4*i])
		h2 = b64.index(data[4*i+1])
		h3 = b64.index(data[4*i+2])
		h4 = b64.index(data[4*i+3])
		bits = h1 << 18 | h2 << 12 | h3 << 6 | h4
		o1 = bits >> 16 & 255
		o2 = bits >> 8 & 255
		o3 = bits & 255
		if h3 == 64: enc += chr(o1)
		elif h4 == 64: enc += chr(o1) + chr(o2)
		else: enc += chr(o1) + chr(o2) + chr(o3)
	return enc

def d(strInput, key):
	strInput = dec(strInput)
	strOutput = ''
	intOffset = (key + 112) / 12
	for i in range(4, len(strInput)):
		thisCharCode = ord(strInput[i])
		newCharCode = thisCharCode - intOffset
		strOutput += chr(newCharCode)
	return strOutput

def decrypt(i, key):
	i = list(i)
	return map(lambda x: d(x, key), i[:3]) + i[-2:]

def bugmenot(type, jid, nick,text):
	global bmn_last_res
	result = ''
	text = text.strip()
	if text:
		conn = httplib.HTTPConnection('www.bugmenot.com')
		conn.request('GET', '/view/' + text.encode("utf-8"))
		r = conn.getresponse().read()
		try: key = int(re.findall('var key = (\d+)',r)[0])
		except: key = ''
		blocked = '<h2>Site Blocked</h2>' in r
		if key and not blocked:
			l = re.findall('<tr><th>Username </th><td><script>d\(\'(.+)\'\);</script></td></tr>\s+?<tr><th>Password </th><td><script>d\(\'(.+?)\'\);</script></td></tr>\s+?<tr><th>Other</th><td><script>d\(\'(.+?)\'\);</script></td></tr>\s+?<tr><th>Stats</th><td class="stats"><em class=".+?">(\d+?)% success rate</em> \((\d+?) votes\)</td></tr>', r)
			l = [decrypt(i, key) for i in l]
			logins = [i[0] for i in l]
			passwords = [i[1] for i in l]
			other = [i[2] for i in l]
			stats = [L('%s%% (%s votes)') % (i[3],i[4]) for i in l]
			data = zip(logins, passwords, other, stats)
			if data:
				first = data[0]
				if bmn_last_res.has_key(jid): bmn_last_res[jid].update({nick: data[1:]})
				else: bmn_last_res[jid] = {nick: data[1:]}
			else: result = L('What?')
		elif blocked: result = L('Site Blocked')
		else: result = L('What?')
	else:
		if bmn_last_res.has_key(jid) and bmn_last_res[jid].has_key(nick) and bmn_last_res[jid][nick]:
			first = bmn_last_res[jid][nick][0]
			bmn_last_res[jid][nick] = bmn_last_res[jid][nick][1:]
		else: result = L('No results!')
	if not result: result = rss_replace(L('Login: %s, Pass: %s - %s %s') % first)
	send_msg(type, jid, nick, result)

def bmn_clear(room,jid,nick,type,arr): 
	if type == 'unavailable' and bmn_last_res.has_key(room) and bmn_last_res[room].has_key(nick): del bmn_last_res[room][nick]

global execute, presence_control

presence_control = [bmn_clear]

execute = [(3, 'bugmenot', bugmenot, 2, L('Search in bugmenot.com'))]

