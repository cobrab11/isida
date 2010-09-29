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

global execute



execute = [(3, 'oracle', oracle, 2, L('Prophecy oracle. Example: oracle your_answer?')),
		(3, 'coin', coin, 2, L('Heads or tails'))]
