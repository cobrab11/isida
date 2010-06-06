#!/usr/bin/python
# -*- coding: utf -*-

def to_poke(type, jid, nick, text):
	if len(text): text = reduce_spaces(text)
	if type == 'chat' and get_level(jid,nick)[0] < 1:
		send_msg(type, jid, nick, L('For members this command not available in private!'))
		return
	predef_poke = [L('gave NICK ... just gave ... :-\"'),
			L('poked a stick NICK in the eye ...'),
			L('suggested NICK shrimp :-['),
			L('fed NICK laxative with powdered glass!'),
			L('whispered in his ear softly NICK LOL!'),
			L('trying kick the ass NICK'),
			L('threw the crowbar aside NICK'),
			L('gave NICK strawberry poison'),
			L('jumped around with a tambourine NICK'),
			L('sticking NICK with the words "buy ice cream, you creep!"')]
	ta = get_level(jid,nick)
	access_mode = ta[0]
	dpoke = getFile(poke_file,predef_poke)
	if text == 'show' and access_mode == 2:
		if type == 'groupchat':
			send_msg(type, jid, nick, L('Sent in private message'))
			type = 'chat'
		msg = L('Phrases:')
		cnt = 1
		for tmp in dpoke:
			msg += '\n'+str(cnt)+'. '+tmp
			cnt += 1
	elif text[:4] == 'del ' and access_mode == 2:
		text = text[4:]
		try: pos = int(text)-1
		except: pos = len(dpoke)+1
		if pos < 0 or pos > len(dpoke): msg = L('The record doesn\'t exist!')
		else:
			remove_body = dpoke[pos]
			dpoke.remove(remove_body)
			writefile(poke_file, str(dpoke))
			msg = L('Removed: %s') % remove_body

	elif text[:4] == 'add ' and access_mode == 2:
		text = text[4:]
		if text.count('NICK'):
			dpoke.append(text)
			writefile(poke_file, str(dpoke))
			msg = L('Added')
		else: msg = L('I can\'t add it! No keyword "NICK"!')
	elif text == '' or text == nick: msg = L('Masochist? 8-D')
	elif get_level(jid,text)[1] == selfjid: msg = L('I ban a ip for such jokes!')
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
			type = 'groupchat'
		else: msg = L('I could be wrong, but %s not is here...') % text
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'poke', to_poke, 2, L('"Poke" command\npoke nick - say a random phrase for nick\nControls command, available only for bot owner:\npoke show - show list of phrases\npoke add phrase - add phrase\npoke del phrase_number - remove phrase.'))]
