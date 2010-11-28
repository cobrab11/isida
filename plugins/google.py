#!/usr/bin/python
# -*- coding: utf -*-

google_last_res = {}

def replace_bold(t,b,e): return t.replace('<b>',b).replace('</b>',e)

def wiki_search(type, jid, nick, text):
	room = jid
	jid = getRoom(get_level(room,nick)[1])
	cof = getFile(conoff,[])
	if (room,'wiki') in cof: return
	tmppos = arr_semi_find(confbase, room)
	nowname = getResourse(confbase[tmppos])
	access_mode = get_level(room,nick)[0]
	if text == 'next': text = 'google next'
	else: text = 'google ' + L('wiki %s inurl:en.wikipedia.org/wiki') % text
	com_parser(access_mode, nowname, type, room, nick, text, jid)

def xep_show(type, jid, nick,text):
	ntext = 'xep '+text+' inurl:xmpp.org'
	url = 'http://ajax.googleapis.com/ajax/services/search/web?'
	search_results = html_encode(load_page(url, {'v': '1.0', 'q': ntext.encode("utf-8")}))
	json = simplejson.loads(search_results)
	try:
		results = json['responseData']['results']
		title = results[0]['title']
		content = results[0]['content']
		noh_title = replace_bold(title,'','')
		content = replace_bold(content,'','')
		msg = '\n'.join((replacer(noh_title),replacer(content),results[0]['unescapedUrl']))
	except: msg = L('xep \"%s\" not found!') % text
	send_msg(type, jid, nick, msg)

def google(type, jid, nick,text):
	global google_last_res
	results = ''
	text = text.strip()
	if text == 'next':
		if google_last_res.has_key(jid) and google_last_res[jid].has_key(nick) and google_last_res[jid][nick]:
			first = google_last_res[jid][nick][0]
			google_last_res[jid][nick] = google_last_res[jid][nick][1:]
		else: results = L('No results!')
	elif text:
		try:
			url = 'http://ajax.googleapis.com/ajax/services/search/web?'
			search_results = html_encode(load_page(url, {'v': '1.0', 'q': text.encode("utf-8")}))
			json = simplejson.loads(search_results)
			data = json['responseData']['results']
			first = data[0]
			if google_last_res.has_key(jid): google_last_res[jid].update({nick: data[1:]})
			else: google_last_res[jid] = {nick: data[1:]}
		except: results = L('Expression \"%s\" not found!') % text
	else: results = L('What?')
	if not results:
		title = first['title']
		content = first['content']
		noh_title = replace_bold(title,u'«',u'»')
		content = replace_bold(content,u'«',u'»')
		url = urllib.unquote(first['unescapedUrl'].encode('utf8')).decode('utf8','ignore')
		results = replacer(noh_title)+'\n'+replacer(content)+'\n'+url
	send_msg(type, jid, nick, results)

def google_clear(room,jid,nick,type,arr): 
	if type == 'unavailable' and google_last_res.has_key(room) and google_last_res[room].has_key(nick): del google_last_res[room][nick]

def translate(type, jid, nick,text):
	text = text.strip()
	trlang = {'sq':L('Albanian'),'en':L('English'),'ar':L('Arabic'),'af':L('Afrikaans'),
			'be':L('Belarusian'),'bg':L('Bulgarian'),'cy':L('Welsh'),'hu':L('Hungarian'),'vi':L('Vietnamese'),
			'gl':L('Galician'),'nl':L('Dutch'),'el':L('Greek'),'da':L('Danish'),'iw':L('Hebrew'),'yi':L('Yiddish'),
			'id':L('Indonesian'),'ga':L('Irish'),'is':L('Icelandic'),'es':L('Spanish'),'it':L('Italian'),
			'ca':L('Catalan'),'zh':L('Chinese'),'ko':L('Korean'),'lv':L('Latvian'),'lt':L('Lithuanian'),
			'mk':L('Macedonian'),'ms':L('Malay'),'mt':L('Maltese'),'de':L('German'),'no':L('Norwegian'),
			'fa':L('Persian'),'pl':L('Polish'),'pt':L('Portuguese'),'ro':L('Romanian'),'ru':L('Russian'),
			'sr':L('Serbian'),'sk':L('Slovak'),'sl':L('Slovenian'),'sw':L('Swahili'),'tl':L('Tagalog'),
			'th':L('Thai'),'tr':L('Turkish'),'uk':L('Ukrainian'),'fi':L('Finnish'),'fr':L('french'),'hi':L('Hindi'),
			'hr':L('Croatian'),'cs':L('Czech'),'sv':L('Swedish'),'et':L('Estonian'),'ja':L('Japanese'),'ht':L('Creole')}
	if text.lower() == 'list': msg = L('Available languages for translate:') + ' ' + ', '.join(trlang.keys())
	elif text[:4].lower() == 'info':
		text = text.lower().split(' ')
		msg = ''
		for tmp in text:
			if tmp in trlang: msg += '%s - %s, ' % (tmp,trlang[tmp])
		if len(msg): msg = L('Available languages: %s') % msg[:-2]
		else: msg = L('I don\'t know this language')
	else:
		if ' ' in text:
			text = text.split(' ',2)
			url = 'http://ajax.googleapis.com/ajax/services/language/translate?'
			if len(text)>1 and trlang.has_key(text[0].lower()):
				if len(text)>2 and trlang.has_key(text[1].lower()): lpair,tr_text = '%s|%s' % (text[0].lower(), text[1].lower()),text[2]
				else: lpair,tr_text = '|%s' % text[0].lower(),' '.join(text[1:])
				search_results = html_encode(load_page(url, {'v' : '1.0', 'q' : tr_text.encode("utf-8"), 'langpair' : lpair}))
				try: json = simplejson.loads(search_results)['responseData']
				except ValueError: json = None
				if json: msg = rss_replace(json['translatedText'])
				else: msg = L('I can\'t translate it!')
			else: msg = L('Incorrect language settings for translate. tr list - available languages.')
		else: msg = L('Command\'s format: tr [from] to text')
	send_msg(type, jid, nick, msg)

global execute, presence_control

presence_control = [google_clear]

execute = [(3, 'tr', translate, 2, L('Translator.\ntr [from_language] to_language text - translate text\ntr list - list for available languages for translate\ntr info <reduction> - get info about language reduction')),
	 (3, 'google', google, 2, L('Search in google')),
	 (3, 'xep', xep_show, 2, L('Search XEP')),
	 (3, 'wiki', wiki_search, 2, L('Search in en.wikipedia.org'))]

