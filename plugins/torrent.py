#!/usr/bin/python
# -*- coding: utf-8 -*-

def GetTorrentInfo(request, tracker, link, count=torrent_default_count):
	url, n = link + urllib.quote(request.encode('utf-8')), 0
	body = html_encode(urllib.urlopen(url).read())
	body = body.split('<table width="100%">')[1].split('</table>')[0].split('<td>')[1:]
	regexp_name = '.*<a href="/torrent/.*">(.*) </a>'
	regexp_size = '</td>.*<td align="right">(.*?)</td>'
	regexp_peers_up = '<img src="http://.*" alt="S|seeders" />&nbsp;(.*)</span>&nbsp;'
	regexp_peers_dn = '<span class="red">&nbsp;(.*)</span>'
	regexp_link = '<a class="downgif" href="(.*?)"><img src'
	output = L('Total results: %s \nTitle ::: Size ::: Peers [up/down]') % \
		str(len(body))
	body = body[:count]	
	if len(body):
		for bbody in body:
			n += 1
			name = re.findall(regexp_name, bbody, re.S)[0]
			size = re.findall(regexp_size, bbody, re.S)[0].replace('&nbsp;', ' ')
			peers_up = re.findall(regexp_peers_up, bbody, re.S)[0]
			peers_dn = re.findall(regexp_peers_dn, bbody, re.S)[0]
			link = re.findall(regexp_link, bbody, re.S)[0]
			output += L('\n%s. %s ::: %s ::: %s/%s\n  Torrent file: %s%s') % \
				(str(n), name, size, peers_up,peers_dn, tracker, link)
	else: output = L('Not found!')		
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
