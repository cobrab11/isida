#!/usr/bin/python
# -*- coding: utf -*-

def exec_ute(type, jid, nick, text):
	try: text = unicode(eval(text))
	except Exception, SM: text = L('I can\'t execute it! Error: %s') % str(SM)
	send_msg(type, jid, nick, text)

def calc(type, jid, nick, text):
	legal = nmbrs+['*','/','+','-','(',')','=','^','!',' ','<','>']
	ppc = 1
	for tt in text:
		all_ok = 0
		for ll in legal:
			if tt==ll:
				all_ok = 1
				break
		if not all_ok:
			ppc = 0
			break
	if text.count('**'): ppc = 0

	if ppc:	
		try: text = str(eval(text))
		except: text = L('I can\'t calculate it')
	else: text = L('Expression unacceptable!')
	send_msg(type, jid, nick, text)

global execute

execute = [(0, u'calc', calc, 2, L('Calculator.')),
	 (2, u'exec', exec_ute, 2, L('Execution of external code.'))]
