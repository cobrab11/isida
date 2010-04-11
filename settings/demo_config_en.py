# -*- coding: utf-8 -*- 

#------------------------------------------------
#             Isida-bot Config file
#                    v1.3en
#------------------------------------------------

Settings = {
'nickname': 		u'<write here bot nick>',					# bot nick in conferences
'jid':				u'isida-jabber-bot@domain.tld/isida-bot',	# bot jid
'password':			u'********',								# password
'status':			u'online',									# bot status chat|online|away|xa|dnd
'priority':			0,											# priority
'message':			u'…а аццкое железко!'}						# status-message

SuperAdmin 		=	u'aaa@bbb.ru'								# bot owner jid
defaultConf		=	u'isida@conference.jabber.ru'				# start conference
prefix			=	u'_'										# command prefix
msg_limit		= 	2048										# limit of the size of messages

#ignore_owner	=	True										# don't allow execute offered commands for bot owner
#debugmode		=	True										# mode _not_to_ignore_an_error_
#dm				=	True										# debugging mode xmpppy
#dm2			=	True										# mode of show of operations of a bot in console
CommandsLog		=	True										# logging commands of a bot
#thread_type	=	None										# threads type thread/threading. default - threading
