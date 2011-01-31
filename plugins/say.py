#!/usr/bin/python
# -*- coding: utf -*-

def say(type, jid, nick, text): send_msg('groupchat', jid, '', to_censore(text))

def psay(type, jid, nick, text):
	nick,text = text.split('\n',1)
	send_msg('chat', jid, nick, to_censore(text))

def gsay(type, jid, nick, text):
	for jjid in confbase: send_msg('groupchat', getRoom(jjid), '', text)

def set_topic(type, jid, nick, text):
	sender(Message(jid, subject=text, typ='groupchat'))
	
def juick_post(type, jid, nick, text):
	send_msg('chat', 'juick@juick.com', '', text)
	sleep(1.2)
	send_msg(type, jid, nick, L('Message posted to Juick.'))
	
global execute

execute = [(6, 'say', say, 2, L('"Say" command. Bot say in conference all text after command.')),
	 (6, 'psay', psay, 2, L('"Say" command. Bot say in private all text after command.\npsay <nick>\ntext')),
	 (9, 'gsay', gsay, 2, L('Global message in all conferences, where bot is present.')),
	 (9, 'juick_post', juick_post, 2, L('Send message to blog at juick.com')),
	 (7, 'topic', set_topic, 2, L('Set conference topic.'))]
