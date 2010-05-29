#!/usr/bin/python
# -*- coding: utf -*-

watch_time = time.time()
watch_count = 0
watch_reset = True

def connect_watch():
	global iq_request, watch_time, game_over, watch_count, bot_exit_type, watch_reset
	if (time.time() - watch_time) > watch_size:
		watch_time = time.time()
		watch_count += 1
		watch_reset = True
		iqid = get_id()
		i = Node('iq', {'id': iqid, 'type': 'get', 'to':selfjid}, payload = [Node('query', {'xmlns': NS_VERSION},[])])
		iq_request[iqid]=(time.time(),watcher_reset,['chat',god,'',''])
		sender(i)
		to = timeout - 10
		while to > 0 and not game_over:
			to -= 1
			sleep(1)
		if watch_reset:
			pprint('Restart by watcher\'s timeout!')
			bot_exit_type, game_over = 'restart', True
			sleep(2)

def watcher_reset(a,b,c,d,e):
	global watch_reset
	watch_reset = None
			
def c_watcher(type, jid, nick): send_msg(type, jid, nick, L('Timeout for ask: %s | Timeout for answer: %s | Last ask: %s | Total checks: %s') % (watch_size,timeout,un_unix(int(time.time() - watch_time)),watch_count))

global execute, timer

timer = [connect_watch]

execute = [(0,'watcher',c_watcher,1,L('Connection activity control.'))]
