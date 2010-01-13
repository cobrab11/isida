#!/usr/bin/python
# -*- coding: utf -*-

watch_size = 600		# период запросов в секундах
watch_timeout = 480		# таймаут соединения в секундах
watch_time = time.time()
watch_count = 0

def connect_watch():
	global iq_answer, watch_size, watch_time, watch_timeout, game_over, watch_count, bot_exit_type
	if (time.time() - watch_time) > watch_size:
		watch_time = time.time()
		watch_count += 1
		iqid = str(randint(1,100000))
		i = Node('iq', {'id': iqid, 'type': 'get', 'to':selfjid}, payload = [Node('query', {'xmlns': NS_VERSION},[])])
		cl.send(i)
		to = watch_timeout
		no_answ = 1
		is_answ = [None]
		while to >= 0 and no_answ:
			for aa in iq_answer:
				if aa[0]==iqid:
					no_answ = 0
					break
			sleep(0.1)
			to -= 0.1
		if to < 0:
			close_age()
			pprint('Restart by watcher\'s timeout!')
			bot_exit_type, game_over = 'restart', True
			sleep(2)

def c_watcher(type, jid, nick):
	msg = u'Таймаут запросов: '+str(watch_size)
	msg += u' | Таймаут ответов: '+str(watch_timeout)
	msg += u' | Последний запрос: '+un_unix(int(time.time() - watch_time))
	msg += u' | Всего проверок: '+str(watch_count)
	send_msg(type, jid, nick, msg)

global execute, timer

timer = [connect_watch]

execute = [(0,'watcher',c_watcher,1,u'Контроль активности соединения.')]
