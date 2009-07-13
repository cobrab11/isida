#!/usr/bin/python
# -*- coding: utf -*-

def to_poke(type, jid, nick, text):
	text = reduce_spaces(text)
	predef_poke = [u'дала NICK... просто дала... :-"',
			u'потыкала палочкой NICK в глаз...',
			u'предложила NICK козявку :-[',
			u'накормила NICK пургеном с толчёным стеклом!',
			u'прошептала NICK в ухо тихонько БУГАГА!',
			u'целится плюсомётом в NICK и добро улыбается...',
			u'кинула ломик в сторону NICK',
			u'дала NICK клубничного йаду',
			u'попрыгала с бубном вокруг NICK',
			u'тыкает NICK со словами "купи мороженного, гадюка!"']
	poke_file = 'plugins/poke.txt'
        ta = get_access(jid,nick)
        access_mode = ta[0]
	dpoke = getFile(poke_file,predef_poke)
	if text == 'show' and access_mode == 2:
		if type == 'groupchat':
			send_msg(type, jid, nick, u'Ушло в приват!')
			type = 'chat'
		msg = u'Фразы:'
		cnt = 1
		for tmp in dpoke:
			msg += '\n'+str(cnt)+'. '+tmp
			cnt += 1
	elif text[:4] == 'del ' and access_mode == 2:
		text = text[4:]
		try:
			pos = int(text)-1
		except:
			pos = len(dpoke)+1
		if pos < 0 or pos > len(dpoke):
			msg = u'Такой записи нет!'
		else:
			remove_body = dpoke[pos]
			dpoke.remove(remove_body)
			writefile(poke_file, str(dpoke))
			msg = u'Удалила: '+remove_body

	elif text[:4] == 'add ' and access_mode == 2:
		text = text[4:]
		if text.count('NICK'):
			dpoke.append(text)
			writefile(poke_file, str(dpoke))
			msg = u'Добавила.'
		else:
			msg = u'Не могу добавить! Нет ключевого слова "NICK"!'
	elif text == '' or text == nick:
		msg = u'Самотык? 8-D'
	elif get_access(jid,text)[1] == selfjid:
		msg = u'Ща зобаню по ip за такие шутки!'
	else:
		is_found = 0
		for tmp in megabase:
			if tmp[0] == jid and tmp[1] == text:
				is_found = 1
				break
		if is_found:
			msg = '/me '+dpoke[randint(0,len(dpoke)-1)]
			msg = msg.replace('NICK',text)
			nick = ''
		else:
			msg = u'Или я дура, или '+text+u' тут нету...'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'poke', to_poke, 2)]
