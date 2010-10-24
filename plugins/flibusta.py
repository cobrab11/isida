#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom.minidom import parseString

def flibusta(type, jid, nick, text):
	text = re.sub(' +', ' ', text).strip()
	msg = ''
	if text == 'new': 
		c=urllib.urlopen('http://xpresslib.mobile-master.org/new').read()
		xml=parseString(c)
		nodes=xml.getElementsByTagName('book')
		for el in nodes:
			f=el.getAttribute('file')
			size=el.getAttribute('size')
			author=unicode(el.getAttribute('author'))
			title=unicode(el.firstChild.data)
			msg += u'\n%s - %s, %s кБ, http://flibusta.net/b/%s' % (author,title,round(float(size)/1024,1),f.split('.')[0]+'/fb2')
		if not msg: msg = L('No news')
	else:
		opt = [i for i in (' ' + text).split(' -') if len(i)>2 and i[1]==' ']
		opt = dict([i.split(' ', 1) for i in opt])
		if opt.has_key('n'):
			if re.match('\d+$', opt['n']): a = b = int(opt['n'])
			elif re.match('\d+-\d+$', opt['n']): a, b = map(int,opt['n'].split('-'))
			else: a, b = 1, 5
		else: a, b = 1, 5
		if opt.has_key('t'):
			i={}
			i['search']=opt['t'].encode('utf-8')
			d=urllib.urlencode(i)
			s=urllib.urlopen('http://xpresslib.mobile-master.org/search',d).read()
			xml=parseString(s)
			nodes=xml.getElementsByTagName('book')
			t_book=[]
			for el in nodes:
				f0=el.getAttribute('file')
				size=el.getAttribute('size')
				author=unicode(el.getAttribute('author'))
				title=unicode(el.firstChild.data)
				t_book.append([author,title,size,f0])
			if opt.has_key('a'): t_book = filter(lambda x: opt['a'].lower() in x[0].lower(), t_book)
			if t_book:
				c = len(t_book)
				if b > c:
					if b != a:  b = c
					else: a = b = c
				msg += L('Total found %s matches. Result(s) %s:\n') % (c, a if a == b else '%s-%s' % (a,b))
 				for i in t_book[a-1:b]:
					msg += u'%s- %s, %s кБ, http://flibusta.net/b/%s\n' % (i[0],i[1],round(float(i[2])/1024,1),i[3].split('.')[0]+'/fb2')
		elif opt.has_key('a'):
			i={}
			i['search']=opt['a'].encode('utf-8')
			d=urllib.urlencode(i)
			s=urllib.urlopen('http://xpresslib.mobile-master.org/authors',d).read()
			xml=parseString(s)
			nodes=xml.getElementsByTagName('author')
			a_book=[]
			for el in nodes:
				id=el.getAttribute('id')
				title=unicode(el.firstChild.data)
				a_book.append([id,title])
			if a_book:
				c = len(a_book)
				if b > c:
					if b != a:  b = c
					else: a = b = c
				msg += L('Total found %s matches. Result(s) %s:\n') % (c, a if a == b else '%s-%s' % (a,b))
				for i in a_book[a-1:b]:
					msg += '%s- http://flibusta.net/a/%s\n' % (i[1], i[0])

	if not msg: msg = L('What?')
	send_msg(type, jid, nick, msg)
		


global execute

execute = [(3, 'flibusta', flibusta, 2, L('Search books and authors on flibusta.net.\nflibusta [-a author] [-t title] [-n number of result]'))]
