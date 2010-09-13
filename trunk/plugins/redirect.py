#!/usr/bin/env python
# -*- coding: utf-8 -*-

def to_private(type, room, nick, text):
	raw_redirect('chat', room, nick, text)

def to_public(type, room, nick, text):
	raw_redirect('groupchat', room, nick, text)

def raw_redirect(type, room, nick, text):
	ta = get_level(room,nick)
	access_mode = ta[0]
	jid =ta[1]
	tmppos = arr_semi_find(confbase, room)
	if tmppos == -1: nowname = nickname
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '': nowname = nickname
	com_parser(access_mode, nowname, type, room, nick, text, jid)

global execute

execute = [(3, 'private', to_private, 2, L('Redirect command output in private.')),
		   (3, 'public', to_public, 2, L('Redirect command output in groupchat.'))]
