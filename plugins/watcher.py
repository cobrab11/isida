#!/usr/bin/python
# -*- coding: utf -*-

watch_size = 900		# период запросов в секундах
watch_timeout = 600		# таймаут соединения в секундах
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
		to, no_answ = watch_timeout, True
		while to >= 0 and no_answ:
			for aa in iq_answer:
				if aa[0]==iqid:
					iq_answer.remove(aa)
					no_answ = None
					break
			sleep(5)
			to -= 5
		if to <= 0:
			pprint('Restart by watcher\'s timeout!')
			bot_exit_type, game_over = 'restart', True
			sleep(2)

def c_watcher(type, jid, nick): send_msg(type, jid, nick, L('Timeout for ask: %s | Timeout for answer: %s | Last ask: %s | Total checks: %s') % (str(watch_size),str(watch_timeout),un_unix(int(time.time() - watch_time)),str(watch_count)))

global execute, timer

timer = [connect_watch]

execute = [(0,'watcher',c_watcher,1,L('Connection activity control.'))]
