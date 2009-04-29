#!/usr/bin/python
# -*- coding: utf -*-

# изменение префикса комманд
preffile = 'settings/prefix'

def update_prefix(old,new,com):
        tcom = []
        for ccom in com:
                ttcom = ccom
                if ccom[1][:len(old)] == old:
                        ttcom = []
                        ttcom.append(ccom[0])
                        ttcom.append(new + ccom[1][len(old):])
                        for tapp in ccom[2:]:
                                ttcom.append(tapp)
                tcom.append(ttcom)
        return tcom

def set_prefix(type, jid, nick, text):
        global preffile, prefix, comms
        old_prefix = prefix
	msg = u'Префикс комманд: '
        if os.path.isfile(preffile):
		pref = eval(readfile(preffile))
		prefix = pref[0]
	else:
		pref = [(u'_')]
		writefile(preffile,pref)
		prefix = pref[0]

        if text != '':
                prefix = text
        msg += prefix
	pref = [(prefix)]
        writefile(preffile,str(pref))
	send_msg(type, jid, nick, msg)

        comms = update_prefix(old_prefix, prefix, comms)

old_prefix = prefix
if os.path.isfile(preffile):
	pref = eval(readfile(preffile))
	prefix = pref[0]
else:
	pref = [(u'_')]
	writefile(preffile,str(pref))
	prefix = pref[0]

comms = update_prefix(old_prefix, prefix, comms)

#------------------------------------------------

# в начале
# 0 - всем
# 1 - админам\овнерам
# 2 - владельцу бота

# в конце
# 0 - передавать параметры
# 1 - ничего не передавать
# 2 - передавать остаток текста

#global execute

execute = [(2, u'prefix', set_prefix, 2)]
