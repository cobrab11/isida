# -*- coding: utf-8 -*- 

#------------------------------------------------
#             Isida-bot Config file
#                  v1.1beta
#------------------------------------------------


# ник бота. !!! нет проверки на занятость ника !!! регистрируем jid и ник, а потом заполняем!
nickname = u'<пишем сюда ник бота>'

# логин бота
name = u'isida-jabber-bot'

# сервер бота
domain = u'domain.tld'

# рессурс бота в конфе
mainRes = u'isida-bot'

# в итоге получим jid бота вида: isida-jabber-bot@domain.tld/isida-bot

# пароль
password = u'********'

# новый jid. 0 - нет. не 0 - да. менять не рекомендуется.
newBotJid = 0

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

# режим _не_игнорировать_ошибки_
#debugmode = 1

# префикс комманд
prefix = u'_'

# режим отладки xmpppy
#dm = 0

# режим показа действий бота в консоле
#dm2 = 0

# Лимит размера сообщений
msg_limit = 1000

# управление ботом минуя owner-лист. функция нужна для возможности мониторинга работы бота. в релизе v1.91 будет полностью убрана из бота!
backdoor = True