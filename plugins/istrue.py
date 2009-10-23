#!/usr/bin/python
# -*- coding: utf -*-

def is_valid(type, jid, nick, text):
	if text == '': text = nick
	ru_lit, en_lit, caps_lit = 0, 0, 0
	for tmp in text:
		if re.match(u'[a-z]|[A-Z]',tmp): en_lit+=1
		elif re.match(u'[а-я]|[А-Я]',tmp): ru_lit+=1
		if re.match(u'[A-Z]|[А-Я]',tmp): caps_lit+=1
	lt = len(text)
	if ru_lit<en_lit: idx, hl = float(ru_lit)/en_lit, 1
	elif ru_lit>en_lit: idx, hl = float(en_lit)/ru_lit, 2
	else: idx, hl = 0.5, None
	if (ru_lit == lt or en_lit == lt) and float(caps_lit)/lt <= 0.5: msg = u'100% Ъ-ник!'
	elif ru_lit+en_lit == 0: msg = u'Ники без букв не Ъ!'
	elif ru_lit+en_lit+text.count(' ')+text.count('.') == lt: msg = u'Кошерность ника - '+str(100-int(idx*100))+u'%'
	elif not ru_lit or not en_lit: msg = u'Нормальный ник, а вот левые символы фтопку!'
	else: msg = u'Кошерность ника - '+str(int(float(ru_lit+en_lit)/lt*100-int(idx*100)))+u'%'
	if float(caps_lit)/lt > 0.5: msg += u' Много капса - '+ str(int(float(caps_lit)/lt*100))+u'%'

	msg += u' Преобладают буквы: '
	if hl == 1: msg += u'Латиница'
	elif hl == 2: msg += u'Кирилица'
	else: msg += u'Поровну'
	send_msg(type, jid, nick, msg)

def is_true(type, jid, nick, text):
	if text == '': msg = u'Ну и?'
	else:
		idx = 0
		for tmp in text: idx += ord(tmp)
		idx = int((idx/100.0 - int(idx/100))*100)
		msg = u'Вероятность того, что выражение верно - '+str(idx)+u'%'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'true', is_true, 2, u'Проверка выражения на правдивость.'),
		   (0, u'valid', is_valid, 2, u'Проверка ника на наличие использования букв из разных языков.')]
