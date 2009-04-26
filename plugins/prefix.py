#!/usr/bin/python
# -*- coding: utf -*-

# изменение префикса комманд
preffile = 'prefix'

def set_prefix(type, jid, nick, text):
        global preffile, prefix
	msg = u'Префикс комманд: '
        if os.path.isfile(preffile):
        	prefix = readfile(preffile)
        else:
        	prefix = '`'
        	writefile(preffile,prefix)

        if text != '':
                prefix = text
        msg += prefix
        writefile(preffile,str(prefix))
	send_msg(type, jid, nick, msg)

if os.path.isfile(preffile):
        prefix = readfile(preffile)
else:
        prefix = '`'
        writefile(preffile,prefix)

#------------------------------------------------

# в начале
# 0 - всем
# 1 - админам\овнерам
# 2 - владельцу бота

# в конце
# 0 - передавать параметры
# 1 - ничего не передавать
# 2 - передавать остаток текста

global execute, prefix

execute = [(2, prefix+u'prefix', set_prefix, 2)]
