#!/usr/bin/python
# -*- coding: utf -*-

def is_valid(type, jid, nick, text):
	if text == '': text = nick
	ru_lit, en_lit, caps_lit = 0, 0, 0
	for tmp in text:
		if re.match('[a-z]|[A-Z]',tmp): en_lit+=1
		elif re.match(u'[а-я]|[А-Я]',tmp): ru_lit+=1
		if re.match(u'[A-Z]|[А-Я]',tmp): caps_lit+=1
	lt = len(text)
	if ru_lit<en_lit: idx, hl = float(ru_lit)/en_lit, 1
	elif ru_lit>en_lit: idx, hl = float(en_lit)/ru_lit, 2
	else: idx, hl = 0.5, None
	if (ru_lit == lt or en_lit == lt) and float(caps_lit)/lt <= 0.5: msg = L('100% True-nick!')
	elif ru_lit+en_lit == 0: msg = L('Nicks without letters isn\'t true!')
	elif ru_lit+en_lit+text.count(' ')+text.count('.') == lt: msg = L('Valid of nick is - %s%s ') % (str(100-int(idx*100)), '%')
	elif not ru_lit or not en_lit: msg = L('Normal nick, but left symbols in fireplace.')
	else: msg = L('Valid of nick is - %s%s ') % (str(int(float(ru_lit+en_lit)/lt*100-int(idx*100))), '%')
	if float(caps_lit)/lt > 0.5: msg += L('Many caps - %s%s ') % (str(int(float(caps_lit)/lt*100)), '%')

	msg += L('Dominate letters:') + ' '
	if hl == 1: msg += L('Latin')
	elif hl == 2: msg += L('Cyrillic')
	else: msg += L('Equally')
	send_msg(type, jid, nick, msg)

def is_true(type, jid, nick, text):
	if text == '': msg = L('And?')
	else:
		idx = 0
		for tmp in text: idx += ord(tmp)
		idx = int((idx/100.0 - int(idx/100))*100)
		msg = L('Expression is true for %s%s') % (str(idx), '%')
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, 'true', is_true, 2, L('Check truth of expession.')),
		   (0, 'valid', is_valid, 2, L('Check different languages symbols in nick.'))]
