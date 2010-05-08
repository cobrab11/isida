#!/usr/bin/python
# -*- coding: utf-8 -*-

youtube_max_videos 		= 10		# максимальное количество ссылок при показе
youtube_default_videos 	= 3			# количество ссылок по умолчанию
youtube_max_page_size 	= 131072	# лимит размера страницы при загрузке
youtube_default_lang 	= 'ru'		# язык по умолчанию

def youtube(type, jid, nick, text):
	if text.count('\n'):
		try: lim = int(text.split('\n',1)[1])
		except: lim = youtube_default_videos
		if lim > youtube_max_videos: lim = youtube_max_videos
		if lim < 1: lim = 1
		text = text.split('\n',1)[0]
	else: lim = youtube_default_videos
	size_overflow = youtube_max_page_size
	text = text.lower().encode('utf-8').replace(' ','%20')
	regex = '<a href="(/watch.*?)".*?<strong class="hovercard-title" >(.*?)</strong>.*?<span class="hovercard-duration">(.*?)</span>.*?<span class="hovercard-upload-date">(.*?)</span>'
	req = urllib2.Request('http://www.youtube.com/results?search_type=&search_query=%s&aq=f&hl=%s' % (text,youtube_default_lang))
	req.add_header('User-Agent',user_agent)
	try: body = str(urllib2.urlopen(req).info())
	except: body = L('I can\'t do it')
	mt = re.findall('Content-Length.*?([0-9]+)', body, re.S)
	msg = None
	if mt != []:
		try:
			c_size = int(''.join(mt[0]))
			if c_size > size_overflow: msg = L('Site size limit overflow! Size - %skb, allowed - %skb') % (c_size/1024,size_overflow/1024)
		except: c_size = size_overflow
	else: c_size = size_overflow
	if not msg:
		try:
			page = remove_sub_space(html_encode(urllib2.urlopen(req).read(c_size))).split('<div class="video-entry yt-uix-hovercard">')
			if len(page) == 1: msg = L('Not found!')
			else:
				try:
					msg = L('Found:')
					for tmp in page[1:lim+1]:
						mt = re.findall(regex, tmp, re.S)
						if mt != []: msg += '\nhttp://youtube.com%s\t%s\t [%s] %s' % mt[0]
				except: msg = L('Not found!')
		except Exception, SM: msg = unicode(SM)
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, 'youtube', youtube, 2, L('Search at YouTube'))]
