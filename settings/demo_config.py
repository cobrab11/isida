# -*- coding: utf-8 -*- 

#------------------------------------------------
#             Isida-bot Config file
#                  v1.2beta
#------------------------------------------------


# ник бота. !!! нет проверки на занятость ника !!! регистрируем jid и ник, а потом заполняем!
# jid бота будет таким: name@domain/mainRes
nickname = u'<пишем сюда ник бота>'

# логин бота
name = u'isida-jabber-bot'

# сервер бота
domain = u'domain.tld'

# рессурс бота в конфе
mainRes = u'isida-bot'

# пароль
password = u'********'

# jid владельца бота
SuperAdmin = u'aaa@bbb.ru'

# стартовая конференция
defaultConf = u'isida@conference.jabber.ru'

# статус бота chat|online|away|xa|dnd
CommStatus = u'online'

# статус-сообщение
StatusMessage = u'Йа аццкое железко!'

# приоритет
Priority = 0

# префикс комманд
prefix = u'_'

# Лимит размера сообщений
msg_limit = 1000

# ------- Отладка! -------

# режим _не_игнорировать_ошибки_
#debugmode = True

# режим отладки xmpppy
#dm = True

# режим показа действий бота в консоле
#dm2 = True

# Логгирование команд бота
CommandsLog = True
