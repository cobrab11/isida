#!/usr/bin/python
# -*- coding: utf -*-

google_last_res = {}

def wiki_search(type, jid, nick,text):
	ntext = L('wiki %s inurl:en.wikipedia.org/wiki') % text
	url = 'http://ajax.googleapis.com/ajax/services/search/web?'
	search_results = html_encode(load_page(url, {'v': '1.0', 'q': ntext.encode("utf-8")}))
	json = simplejson.loads(search_results)
	try:
		results = json['responseData']['results']
		title = results[0]['title']
		content = results[0]['content']
		noh_title = title.replace('<b>', '').replace('</b>', '')
		content = content.replace('<b>', '').replace('</b>', '')
		url = results[0]['unescapedUrl']
		url = urllib.unquote(url.encode('utf8')).decode('utf8')
		msg = replacer(noh_title)+'\n'+replacer(content)+'\n'+url
	except: msg = L('Expression \"%s\" not found!') % text
	send_msg(type, jid, nick, msg)

def xep_show(type, jid, nick,text):
	ntext = 'xep '+text+' inurl:xmpp.org'
	url = 'http://ajax.googleapis.com/ajax/services/search/web?'
	search_results = html_encode(load_page(url, {'v': '1.0', 'q': ntext.encode("utf-8")}))
	json = simplejson.loads(search_results)
	try:
		results = json['responseData']['results']
		title = results[0]['title']
		content = results[0]['content']
		noh_title = title.replace('<b>', '').replace('</b>', '')
		content = content.replace('<b>', '').replace('</b>', '')
		url = results[0]['unescapedUrl']
		msg = replacer(noh_title)+'\n'+replacer(content)+'\n'+url
	except: msg = L('xep \"%s\" not found!') % text
	send_msg(type, jid, nick, msg)

def google(type, jid, nick,text):
	results = ''
	global google_last_res
	text = text.strip()
	if text == 'next':
		if google_last_res.has_key(jid) and google_last_res[jid].has_key(nick) and google_last_res[jid][nick]:
			first = google_last_res[jid][nick][0]
			google_last_res[jid][nick] = google_last_res[jid][nick][1:]
		else:
			results = L('No results!')
	elif text:
		try:
			url = 'http://ajax.googleapis.com/ajax/services/search/web?'
			search_results = html_encode(load_page(url, {'v': '1.0', 'q': text.encode("utf-8")}))
			json = simplejson.loads(search_results)
			data = json['responseData']['results']
			first = data[0]
			if google_last_res.has_key(jid):
				google_last_res[jid].update({nick: data[1:]})
			else:
				google_last_res[jid] = {nick: data[1:]}
		except: results = L('Expression \"%s\" not found!') % text
	else: results = L('What?')
	if not results:
		title = first['title']
		content = first['content']
		noh_title = title.replace('<b>', u'«').replace('</b>', u'»')
		content = content.replace('<b>', u'«').replace('</b>', u'»')
		url = first['unescapedUrl']
		url = urllib.unquote(url.encode('utf8')).decode('utf8')
		results = replacer(noh_title)+'\n'+replacer(content)+'\n'+url
	send_msg(type, jid, nick, results)

def google_clear(room,jid,nick,type,arr): 
	if type == 'unavailable' and google_last_res.has_key(room) and google_last_res[room].has_key(nick):
		del google_last_res[room][nick]

def translate(type, jid, nick,text):
	trlang = {'sq':L('Albanian'),'en':L('English'),'ar':L('Arabic'),'af':L('Afrikaans'),
			  'be':L('Belarusian'),'bg':L('Bulgarian'),'cy':L('Welsh'),'hu':L('Hungarian'),'vi':L('Vietnamese'),
			  'gl':L('Galician'),'nl':L('Dutch'),'el':L('Greek'),'da':L('Danish'),'iw':L('Hebrew'),'yi':L('Yiddish'),
			  'id':L('Indonesian'),'ga':L('Irish'),'is':L('Icelandic'),'es':L('Spanish'),'it':L('Italian'),
			  'ca':L('Catalan'),'zh':L('Chinese'),'ko':L('Korean'),'lv':L('Latvian'),'lt':L('Lithuanian'),
			  'mk':L('Macedonian'),'ms':L('Malay'),'mt':L('Maltese'),'de':L('German'),'no':L('Norwegian'),
			  'fa':L('Persian'),'pl':L('Polish'),'pt':L('Portuguese'),'ro':L('Romanian'),'ru':L('Russian'),
			  'sr':L('Serbian'),'sk':L('Slovak'),'sl':L('Slovenian'),'sw':L('Swahili'),'tl':L('Tagalog'),
			  'th':L('Thai'),'tr':L('Turkish'),'uk':L('Ukrainian'),'fi':L('Finnish'),'fr':L('french'),'hi':L('Hindi'),
			  'hr':L('Croatian'),'cs':L('Czech'),'sv':L('Swedish'),'et':L('Estonian'),'ja':L('Japanese')}
	if text.lower() == 'list':
		msg = L('Available languages for translate:') + ' '
		for tl in trlang: msg += tl+', '
		msg = msg[:-2]
	elif text[:4].lower() == 'info':
		text = text.lower().split(' ')
		msg = ''
		for tmp in text:
			if tmp in trlang: msg += tmp+' - '+trlang[tmp]+', '
		if len(msg): msg = L('Available languages: %s') % msg[:-2]
		else: msg = L('I don\'t know this language')
	else:
		if text.count(' ') > 1:
			text = text.split(' ',2)
			if (text[0].lower() in trlang) and (text[1].lower() in trlang) and text[2] != '':
				url = 'http://ajax.googleapis.com/ajax/services/language/translate?'
				lpair = '%s|%s' % (text[0].lower(), text[1].lower())
				search_results = html_encode(load_page(url, {'v' : '1.0', 'q' : text[2].encode("utf-8"), 'langpair' : lpair}))
				json = simplejson.loads(search_results)
				msg = rss_replace(json['responseData']['translatedText'])
			else: msg = L('Incorrect language settings for translate. tr list - available languages.')
		else: msg = L('Command\'s format: tr from to text')
	send_msg(type, jid, nick, msg)

global execute, presence_control

execute = [(3, 'tr', translate, 2, L('Translator.\ntr from_language to_language text - translate text\ntr list - list for available languages for translate\ntr info <reduction> - get info about language reduction')),
	 (3, 'google', google, 2, L('Search in google')),
	 (3, 'xep', xep_show, 2, L('Search XEP')),
	 (3, 'wiki', wiki_search, 2, L('Search in en.wikipedia.org'))]
presence_control = [google_clear]
