#!/usr/bin/python
# -*- coding: utf -*-

def test(type, jid, nick):
	2/0
	send_msg(type, jid, nick, L('Passed!'))

global execute

execute = [(0, 'test', test, 1, L('Check bot activity.'))]
