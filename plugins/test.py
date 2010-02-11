#!/usr/bin/python
# -*- coding: utf -*-

def test(type, jid, nick):
	send_msg(type, jid, nick, L('Passed!'))

global execute

execute = [(0, u'test', test, 1, L('Check bot activity.'))]
