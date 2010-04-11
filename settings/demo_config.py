# -*- coding: utf-8 -*- 

#------------------------------------------------
#             Isida-bot Config file
#                    v1.3ru
#------------------------------------------------

Settings = {
'nickname': 		u'<пишем сюда ник бота>',					# Ник бота в конференциях
'jid':				u'isida-jabber-bot@domain.tld/isida-bot',	# Jid бота
'password':			u'********',								# Пароль
'status':			u'online',									# Статус бота chat|online|away|xa|dnd
'priority':			0,											# Приоритет
'message':			u'Йа аццкое железко!'}						# Статус-сообщение

SuperAdmin		=	u'aaa@bbb.ru'								# Jid владельца бота
defaultConf		=	u'isida@conference.jabber.ru'				# Стартовая конференция
prefix			=	u'_'										# Префикс комманд по умолчанию
msg_limit		=	2048										# Лимит размера сообщений

#ignore_owner	=	True										# не исполнять для владельца бота отключенные команды
#debugmode		=	True										# режим _не_игнорировать_ошибки_
#dm				=	True										# режим отладки xmpppy
#dm2			=	True										# режим показа действий бота в консоле
CommandsLog		=	True										# Логгирование команд бота
#thread_type	=	None										# тип тредов thread/threading. по умолчанию - threading
