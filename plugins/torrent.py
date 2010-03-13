#!/usr/bin/python
# -*- coding: utf-8 -*-

def GetTorrentInfo(request, tracker, link, count=3):
	url, n = link + urllib.quote(request.encode('utf-8')), 0
	body = html_encode(urllib.urlopen(url).read())
	body = body.split('<table width="100%">')[1].split('</table>')[0]
	body = body.replace('&nbsp;', ' ').split('<td>')[1:]
	output = L('Total results: %s \nTitle ::: Size ::: Peers [up/down]') % \
		str(len(body))
	body = body[:count]	
	for tmp in body:
		n += 1
		tmp = tmp.split('</td>')
		if len(tmp) == 6: tmp.remove(tmp[2])
		output += u'\n' + str(n) + u'. ' + replacer(tmp[1]) + u' ::: ' + \
			replacer(tmp[2]) + u' :::'+ rss_del_html(tmp[3]).replace('  ', '/')
		output += u'\n  Torrent файл: %s' % tracker
		ttmp = tmp[1][tmp[1].find('/download'):]
		ttmp = ttmp[:ttmp.find('">')]
		if tracker == 'http://opensharing.org': ttmp = ttmp[:-1]
		output += ttmp
	return output

def torrent_main(type, jid, nick, text):
	comms = ['rutor', 'os']
	text = text.split('\n')
	try:
		if text[0] in comms:
			if text[0] == comms[0]:
				tracker = u'http://rutor.org'
				url = u'http://rutor.org/search/'
			elif text[0] == comms[1]:
				tracker = u'http://opensharing.org'
				url = u'http://opensharing.org/b.php?search='
			try: msg = GetTorrentInfo(text[1], tracker, url, int(text[2]))
			except: msg = GetTorrentInfo(text[1], tracker, url)
			if len(msg) > msg_limit:
				send_msg(type, jid, nick, L('Send for you in private'))
				type = 'chat'
		else: msg = L('Incorrect tracker.')
	except: msg = L('Command execution error.')
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'torrent', torrent_main, 2, L('Search in bittorrent trackers\ntorrent rutor - search in RuTor.org\ntorrent os - search in OpenSharing.org\ntorrent tracker\nquery\ncount'))]
