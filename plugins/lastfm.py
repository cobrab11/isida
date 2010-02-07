# -*- coding: utf-8 -*-

global execute, lf_api, lfm_url, lfm_api, timer

lfm_url = u'http://ws.audioscrobbler.com/2.0/'

def last_time_short(tm):
	tm = time.localtime(tm)
	tnow = time.localtime()
	if tm[0] != tnow[0]: form = '%d.%m.%Y %H:%M'
	elif tm[1]!=tnow[1] or tm[2]!=tnow[2]: form = '%d.%m %H:%M'
	else: form = '%H:%M'
	return str(time.strftime(form,tm))

def last_date_now(body):
	ldate = get_tag(body,'date')
	if ldate.count('nowplaying=\"true\"'): return 'now'
	else: 
		try: return last_time_short(int(get_subtag(get_tag_full(body,'date'),'uts')))
		except: return u'Unknown'

def lastonetrack(type, jid, nick, text):
	ms = lf_api('user.getrecenttracks',text, '<track')
	if len(ms): cnt = len(ms)
	else: cnt = 0
	if cnt >=2: msg = L('Last track %s: %s – %s [%s]') % (text,get_tag(ms[1],'artist'),get_tag(ms[1],'name'),last_date_now(ms[1]))
	else: msg = L('Unavailable!')
	send_msg(type, jid, nick, msg)

def lf_api(method, user, splitter):
	user = user.lower().encode('utf-8').replace('\\x','%').replace(' ','%20')
	link = lfm_url + '?method=' + method + '&user=' + user + '&api_key='+lfm_api
	f = urllib.urlopen(link)
	lfxml = f.read()
	f.close()
	return rss_replace(html_encode(lfxml)).split(splitter)

def lasttracks(type, jid, nick, text):
	text = text.split(' ')
	try: cnt = int(text[1])
	except: cnt = 10
	cnt += 1
	text = text[0]
	ms = lf_api('user.getrecenttracks',text, '<track')
	if cnt > len(ms): cnt = len(ms)
	msg = L('Last tracks %s:') % text
	for a in ms[1:cnt]: msg += '\n['+last_date_now(a)+'] '+get_tag(a,'artist')+u' – '+get_tag(a,'name')
	send_msg(type, jid, nick, msg)

def lastfriends(type, jid, nick, text):
	ms = lf_api('user.getfriends',text, '<user')
	msg = L('Loved tracks %s:') % text
	for a in ms[1:]:
		msg += ' ' + get_tag(a,'name')+' ('+get_tag(a,'realname')+u'),'
	msg = msg[:-1]
	send_msg(type, jid, nick, msg)

def lastloved(type, jid, nick, text):
	text = text.split(' ')
	try: cnt = int(text[1])
	except: cnt = 10
	cnt += 1
	text = text[0]
	ms = lf_api('user.getlovedtracks',text, '<track')
	if cnt > len(ms): cnt = len(ms)
	msg = L('Loved tracks %s:') % text
	for a in ms[1:cnt]: msg += '\n['+last_date_now(a)+'] '+get_tag(a.split('<artist')[1],'name')+u' – '+get_tag(a,'name')
	send_msg(type, jid, nick, msg)

def lastneighbours(type, jid, nick, text):
	text = text.split(' ')
	try: cnt = int(text[1])
	except: cnt = 10
	cnt += 1
	text = text[0]
	ms = lf_api('user.getneighbours',text, '<user')
	if cnt > len(ms): cnt = len(ms)
	msg = L('Neighbours %s:') % text
	for a in ms[1:cnt]: msg += '\n'+get_tag(a,'match')+u' – '+get_tag(a,'name')
	send_msg(type, jid, nick, msg)

def lastplaylist(type, jid, nick, text):
	text = text.split(' ')
	try: cnt = int(text[1])
	except: cnt = 10
	cnt += 2
	text = text[0]
	ms = lf_api('user.getplaylists',text, '<playlist')
	if cnt > len(ms): cnt = len(ms)
	msg = L('Playlists %s:') % text
	for a in ms[2:cnt]: msg += '\n['+get_tag(a,'id')+'] '+get_tag(a,'title')+' ('+get_tag(a,'description')+u') – '+get_tag(a,'size')+u' – '+get_tag(a,'duration')
	send_msg(type, jid, nick, msg)

def topalbums(type, jid, nick, text):
	text = text.split(' ')
	try: cnt = int(text[1])
	except: cnt = 10
	cnt += 1
	text = text[0]
	ms = lf_api('user.gettopalbums',text, '<album')
	if cnt > len(ms): cnt = len(ms)
	msg = L('Top albums %s:') % text
	for a in ms[1:cnt]: msg += '\n['+get_tag(a,'playcount')+'] '+get_tag(a.split('<artist')[1],'name')+u' – '+get_tag(a,'name')
	send_msg(type, jid, nick, msg)

def topartists(type, jid, nick, text):
	text = text.split(' ')
	try: cnt = int(text[1])
	except: cnt = 10
	cnt += 1
	text = text[0]
	ms = lf_api('user.gettopartists',text, '<artist')
	if cnt > len(ms): cnt = len(ms)
	msg = L('Top artists %s:') % text
	for a in ms[1:cnt]: msg += '\n['+get_tag(a,'playcount')+'] '+get_tag(a,'name')
	send_msg(type, jid, nick, msg)

def toptags(type, jid, nick, text):
	text = text.split(' ')
	try: cnt = int(text[1])
	except: cnt = 10
	cnt += 1
	text = text[0]
	ms = lf_api('user.gettoptags',text, '<tag')
	if cnt > len(ms): cnt = len(ms)
	msg = L('Top tags %s:') % text
	for a in ms[1:cnt]: msg += '\n['+get_tag(a,'count')+'] '+get_tag(a,'name')+u' – '+get_tag(a,'url')
	send_msg(type, jid, nick, msg)

def toptracks(type, jid, nick, text):
	text = text.split(' ')
	try: cnt = int(text[1])
	except: cnt = 10
	cnt += 1
	text = text[0]
	ms = lf_api('user.gettoptracks',text, '<track')
	if cnt > len(ms): cnt = len(ms)
	msg = L('Top tracks %s:') % text
	for a in ms[1:cnt]:
		b = a.split('<artist')
		msg += '\n['+get_tag(a,'playcount')+'] '+get_tag(b[1],'name')+u' – '+get_tag(a,'name')
	send_msg(type, jid, nick, msg)

def tasteometer(type, jid, nick, text):
	text = text.lower().encode('utf-8').replace('\\x','%').split(' ')
	try:
		user1 = text[0]
		user2 = text[1]
	except:
		send_msg(type, jid, nick, L('Need two users'))
		return
	link = lfm_url + '?method=tasteometer.compare&type1=user&type2=user&value1=' + user1 + '&value2=' + user2 + '&api_key='+lfm_api
	f = urllib.urlopen(link)
	lfxml = f.read()
	f.close()
	lfxml = html_encode(lfxml)
	scor = get_tag(lfxml,'score')
	try: scor = float(scor)
	except: scor = 0
	if scor <= 0: msg = L('Tastes of %s and %s - soo different!') % (user1,user2)
	else:
		msg = L('Match tastes of %s and %s - %s') % (user1,user2,str(int(scor*100))+'%') 
		msg2 = ''
		lfxml = lfxml.split('<artist')
		cnt = len(lfxml)
		for a in lfxml[2:cnt]: msg2 += get_tag(a,'name')+', '
		if len(msg2): msg += '\n'+L('Artists: %s') % msg2[:-2]
	send_msg(type, jid, nick, msg)

def no_api(type, jid, nick):
	send_msg(type, jid, nick, L('Not found file LastFM.api'))

apifile = 'plugins/LastFM.api'

exec_yes = [(0, u'lasttracks', lasttracks, 2, L('Last scrobled tracks')),
	    (0, u'last', lastonetrack, 2, L('Last scrobled track')),
	    (0, u'lastfriends', lastfriends, 2, L('Last friends')),
	    (0, u'lastloved', lastloved, 2, L('Last loved tracks')),
	    (0, u'lastneighbours', lastneighbours, 2, L('Last neighbours')),
	    (0, u'lastplaylist', lastplaylist, 2, L('Last playlist')),
	    (0, u'topalbums', topalbums, 2, L('Top albums')),
	    (0, u'topartists', topartists, 2, L('Top artists')),
	    (0, u'toptags', toptags, 2, L('Top tags')),
	    (0, u'toptracks', toptracks, 2, L('Top tracks')),
	    (0, u'tasteometer', tasteometer, 2, L('Music tastes'))]

exec_no = [(0, u'lasttracks', no_api, 1, L('Not found file LastFM.api')),
	   (0, u'last', no_api, 1, L('Not found file LastFM.api')),
	   (0, u'lastfriends', no_api, 1, L('Not found file LastFM.api')),
	   (0, u'lastloved', no_api, 1, L('Not found file LastFM.api')),
	   (0, u'lastneighbours', no_api, 1, L('Not found file LastFM.api')),
	   (0, u'lastplaylist', no_api, 1, L('Not found file LastFM.api')),
	   (0, u'topalbums', no_api, 1, L('Not found file LastFM.api')),
	   (0, u'topartists', no_api, 1, L('Not found file LastFM.api')),
	   (0, u'toptags', no_api, 1, L('Not found file LastFM.api')),
	   (0, u'toptracks', no_api, 1, L('Not found file LastFM.api')),
	   (0, u'tasteometer', no_api, 1, L('Not found file LastFM.api'))]

if os.path.isfile(apifile):
	lfm_api = str(readfile(apifile))
	if len(lfm_api) >= 30: execute = exec_yes
	else: execute = exec_no
else: execute = exec_no


