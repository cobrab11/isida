#!/usr/bin/python
# -*- coding: utf -*-

def google(type, jid, nick,text):
	query = urllib.urlencode({'q' : text.encode("utf-8")})
	url = u'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s'.encode("utf-8") % (query)
	search_results = urllib.urlopen(url)
	json = simplejson.loads(search_results.read())
	try:
		results = json['responseData']['results']
		title = results[0]['title']
		content = results[0]['content']
		noh_title = title.replace('<b>', u'«').replace('</b>', u'»')
		content = content.replace('<b>', u'«').replace('</b>', u'»')
		url = results[0]['unescapedUrl']
		msg = replacer(noh_title)+replacer(content)+url
	except:
		msg = u'Выражение "' + text + u'" - не найдено!'
	send_msg(type, jid, nick, msg)

def translate(type, jid, nick,text):
	trlang = ['sq','ar','bg','ca','zh-CN','zh-TW','hr','cs','da',
		  'nl','en','et','tl','fi','fr','gl','de','el','iw',
		  'hi','hu','id','it','ja','ko','lv','lt','mt','no',
		  'pl','pt','ro','ru','sr','sk','sl','es','sv','th','tr','uk','vi']
	if text.lower() == 'list':
		msg = u'Доступные языки для перевода: '
		for tl in trlang:
			msg += tl+', '
		msg = msg[:-2]
	else:
		if text.count(' ') > 1:
			text = text.split(' ',2)
			if trlang.count(text[0]) and trlang.count(text[1]) and text[2] != '':
				query = urllib.urlencode({'q' : text[2].encode("utf-8"),'langpair':text[0]+'|'+text[1]})
				url = u'http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&%s'.encode("utf-8") % (query)
				search_results = urllib.urlopen(url)
				json = simplejson.loads(search_results.read())
				msg = json['responseData']['translatedText']
			else:
				msg = u'Неправильно указан язык или нет текста для перевода. tr list - доступные языки'
		else:
			msg = u'Формат команды: tr с_какого на_какой текст'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'tr', translate, 2, u'Переводчик.\ntr с_какого_языка на_какой_язык текст - перевод текста\ntr list - список языков для перевода'),
	 (0, u'google', google, 2, u'Поиск через google')]
