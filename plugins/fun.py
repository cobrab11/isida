#!/usr/bin/python
# -*- coding: utf-8 -*-

def oracle(type, jid, nick, text):
	if not text.strip() or text.strip()[-1] != '?': msg = L('What?')
	else: msg = random.choice([L('Yes'),
			L('Yes - definitely'),
			L('You may rely on it'),
			L('Without a doubt'),
			L('Signs point to yes'),
			L('Outlook good'),
			L('Most likely'),
			L('It is decidedly so'),
			L('It is certain'),
			L('As I see it, yes'),
			L('Reply hazy, try again'),
			L('Ask again later'),
			L('Better not tell you now'),
			L('Cannot predict now'),
			L('Concentrate and ask again'),
			L('Don\'t count on it'),
			L('My reply is no'),
			L('Outlook not so good'),
			L('My sources say no')])
	send_msg(type, jid, nick, msg)	

def coin(type, jid, nick, text):
	msg = random.choice([L('Head'), L('Tail')])
	send_msg(type, jid, nick, msg)
	
def to_poke(type, jid, nick, text):
	if len(text): text = reduce_spaces(text)
	if type == 'chat' and get_level(jid,nick)[0] < 7:
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
	if text == 'show' and access_mode == 9:
		if type == 'groupchat':
			send_msg(type, jid, nick, L('Sent in private message'))
			type = 'chat'
		msg = L('Phrases:')
		cnt = 1
		for tmp in dpoke:
			msg += '\n'+str(cnt)+'. '+tmp
			cnt += 1
	elif text[:4] == 'del ' and access_mode == 9:
		text = text[4:]
		try: pos = int(text)-1
		except: pos = len(dpoke)+1
		if pos < 0 or pos > len(dpoke): msg = L('The record doesn\'t exist!')
		else:
			remove_body = dpoke[pos]
			dpoke.remove(remove_body)
			writefile(poke_file, str(dpoke))
			msg = L('Removed: %s') % remove_body

	elif text[:4] == 'add ' and access_mode == 9:
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

def life(type, jid, nick, text):
	tmp = text.split(' ')
	d,m,y = tmp[0].strip().split('.')
	y = int(y)
	if y<20: y += 2000
	elif y<100: y += 1900
	y = str(y)
	if len(tmp)>1: hour, minute, sec = tmp[1].strip().split(':')
	else: hour, minute, sec = '00','00','00'
	BDate = time.mktime(time.strptime(' '.join([y, m, d, hour, minute, sec]), '%Y %m %d %H %M %S'))
	CDate = time.time()
	Age = CDate-BDate
	yrs = int(round(Age/31557600))
	dys = int(round(Age/86400))
	hrs = int(round(Age/3600))
	mins = int(round(Age/60))
	secs = int(round(Age))
	spal = int(round(Age*3285/31557600))
	spal24 = int(round(Age*136.9/31557600))
	morgnyl = int(round(Age*4160000/31557600))
	serdcelit = int(round(Age*2372500/31557600))
	serdceraz = int(round(Age*36500000/31557600))
	vodal = int(round(Age*750/31557600))
	voda = int(round(Age*21/31557600))
	volosicm = int(round(Age*18/31557600))
	volosi = int(round(Age*25550/31557600))
	volosivse = int(round(Age*14/31557600))
	nogtiryk = int(round(Age*5.2/31557600))
	nogtinog = int(round(Age*1.4/31557600))
	vozdyx = int(round(Age*3784320/31557600))
	vozdyxkg = int(round(Age*4881/31557600))
	pot = int(round(Age*252/31557600))
	mochalit = int(round(Age*489/31557600))
	sluni = int(round(Age*337/31557600))
	nervi = int(round(Age*136/31557600))
	smex = int(round(Age*5475/31557600))
	km = int(round(Age*1857/31557600))
	msg = L('You live %s years or %s days or %s hours or %s minutes or %s seconds.\nYou slept %s hours, or %s days.\nYou blink about %s times.\nYour heart pumped %s liters of blood and made %s strikes.\nYou drank %s liters of water and drank it %s hours.\nYou have increased by %s centimeters in my head of hair, dropped %s pieces, all of the hair %s kilometers.\nYou grew up in the hands %s centimeters and in the feet %s centimeters nails.\nYou breathed %s liters of air a total weight of %s kilograms.\nYou have stood out %s liters of sweat, and %s liters of urine, and %s liters of saliva.\nYou lost %s billion nerve cells.\nYou laughed %s times.\nYou\'ve gone %s kilometers') % (yrs, dys, hrs, mins, secs, spal, spal24, morgnyl, serdcelit, serdceraz, vodal, voda, volosicm, volosi, volosivse, nogtiryk, nogtinog, vozdyx, vozdyxkg, pot, mochalit, sluni, nervi, smex, km)
	if type == 'groupchat': send_msg(type, jid, nick, L('Send for you in private'))
	send_msg('chat', jid, nick, msg)

global execute

execute = [(3, 'oracle', oracle, 2, L('Prophecy oracle. Example: oracle your_answer?')),
		(3, 'coin', coin, 2, L('Heads or tails')),
		(3, 'poke', to_poke, 2, L('"Poke" command\npoke nick - say a random phrase for nick\nControls command, available only for bot owner:\npoke show - show list of phrases\npoke add phrase - add phrase\npoke del phrase_number - remove phrase.')),
		(3, 'life', life, 2, L('Info about your life. Example: life dd.mm.yy [hour:min:sec]'))]
