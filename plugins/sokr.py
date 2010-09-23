#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Vit@liy

def sokr(type, jid, nick, text):
	if not text.strip(): msg = L('What?')
	else:
		if re.search('\A\d+?(-\d+?)? ', text): target, text = text.split(' ', 1)
		query=urllib.urlencode({'q':text.encode('utf-8')})
		sokr=httplib.HTTPConnection("www.sokr.ru")
		sokr.request("GET","/search/?abbr=%s&abbr_exact=1" % query)
		search=sokr.getresponse()
		data=search.read()
		results = re.findall('em class="got_clear">.+?</em></a>.+?<p class="value">(.+?)</p>' , data, re.S)
		cr = len(results)
		if not results: msg = L('I don\'t know!')
		else:
			if cr == 1: target = '1'
			else:  target = '1-%s' % cr
			try: n1 = n2 = int(target)
			except: n1, n2 = map(int, target.split('-'))
			if 0 < n1 <= n2 <= cr: 
				msg = L('Total found %s matches. Result(s) %s:\n') % (cr, target)	
				count = n1-1
				for k in xrange(n1-1, n2):
					count += 1
					msg += '%s) %s\n' % (count, results[k].decode('utf8'))
				msg = msg.replace('<br>', '')
			else: msg = L('I don\'t know!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'sokr', sokr, 2, L('Abbreviations.\nExamples: sokr abbr, sokr 6 abbr, sokr 3-7 abbr'))]
