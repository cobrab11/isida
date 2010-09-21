#!/usr/bin/python
# -*- coding: utf -*-

bomb_colors = [L('blue'),L('red'),L('magenta'),L('green'),L('cyan'),L('yellow'),L('white'),L('black')]
bomb_current = {}
bomb_timer = 30
bomb_colors_number = 4
bomb_fault_persent = 25
bomb_random_sleep = 600
bomb_random_list = {}
bomb_random_timer_def = 1800
bomb_random_timer_persent_def = 25
bomb_random_timer_skip_persent_def = 25
bomb_random_timer_check_period = 10
bomb_deny_access = [-1,9]
bomb_last_activity = {}
bomb_idle_default = 900

def bomb_idle(jid,nick):
	global idle_base
	for tmp in idle_base:
		if tmp[0] == jid and tmp[1] == nick:
			try: bid = int(get_config(getRoom(jid),'bomb_idle'))
			except: bid = bomb_idle_default
			if int(time.time())-tmp[3] >= bid: break
			else: return False
	return True

def boom_bomb(room,type,nick,bc,mode):
	b_fault = None
	if get_config(getRoom(room),'bomb_fault'):
		try: bfp = int(get_config(getRoom(room),'bomb_fault_persent'))
		except: bfp = bomb_fault_persent
		if bfp < 0 or bfp > 100: bfp = bomb_fault_persent
		b_fault = random.randint(0,100) < bfp
	if b_fault: send_msg(type, room, nick, L('It\'s a lucky day for you! Bomb is fault! Right wide is %s') % bc)
	else:
		if mode: send_msg(type, room, nick, L('You were wrong! Right wire is %s') % bc)
		if get_config(getRoom(room),'bomb_action') == 'kick': muc_role(type, room, nick, '%s\n%s' % (nick,get_config(getRoom(room),'bomb_reason')), 'none')

def get_next_random(room):
	try: btm = int(get_config(room,'bomb_random_timer'))
	except: btm = bomb_random_timer_def
	if btm < 0: btm = bomb_random_timer_def
	try: btmp = int(get_config(room,'bomb_random_timer_persent'))
	except: btmp = bomb_random_timer_persent_def
	if btmp <= 0 or btmp > 99: btmp = bomb_random_timer_persent_def
	btm_pers = int(btm/100*btmp)
	try: bskp = int(get_config(room,'bomb_random_timer_skip_persent'))
	except: bskp = bomb_random_timer_skip_persent_def
	if bskp <= 0 or bskp > 99: bskp = bomb_random_timer_skip_persent_def
	if random.randint(0,100) > bskp: btm *= 2
	return time.time() + btm + random.randint(-btm_pers,btm_pers)

def bomb_joke(type, jid, nick, text):
	global bomb_current,bomb_random_list
	if type == 'chat':
		send_msg(type, jid, nick, L('Not allowed in private!'))
		return
	if len(text) == 0 or len(text) == text.count(' ')+text.count('\n'):
		rlist,tconf = [],getRoom(jid)
		for tm in megabase:
			if tm[0] == tconf and not bomb_idle(jid,text) and not (get_level(tconf,tm[1])[0] in bomb_deny_access) and not (getRoom(get_level(tconf,tm[1])[1]) in ['None',getRoom(selfjid)]): rlist.append(tm[1])
		text = rlist[random.randrange(len(rlist))]
	bmb = False
	if not get_config(getRoom(jid),'bomb'): msg = L('In this room not allowed take a bomb!')
	elif jid in bomb_current.keys(): msg = L('This room alredy boombed!')
	elif bomb_idle(jid,text) or get_level(jid,text)[0] in bomb_deny_access or getRoom(get_level(jid,text)[1]) in ['None',getRoom(selfjid)]: msg = L('I can\'t take a bomb to %s') % text
	else:					
		try: b_timer = int(get_config(getRoom(jid),'bomb_timer'))
		except: b_timer = bomb_timer
		if b_timer < 0: b_timer = bomb_timer
		try: b_wire = int(get_config(getRoom(jid),'bomb_wire'))
		except: b_wire = bomb_colors_number
		if b_wire < 3 or b_wire > len(bomb_colors): b_wire = bomb_colors_number
		b_clrs = []
		while len(b_clrs) < b_wire:
			bc = bomb_colors[random.randrange(len(bomb_colors))]
			if bc not in b_clrs: b_clrs.append(bc)
		bomb_current[getRoom(jid)] = [text,b_clrs,b_clrs[random.randrange(len(b_clrs))]]
		msg,bmb = L('/me take a bomb to %s with wires %s. Time to deactivate is %s sec.') % (text,', '.join(b_clrs),b_timer),True
	send_msg(type, jid, '', msg)
	if bmb:
		while b_timer > 0 and not game_over:
			sleep(1)
			b_timer -= 1
			if jid not in bomb_current.keys(): break
		if b_timer <= 0 and not game_over:
			bc = bomb_current.pop(getRoom(jid))                     
			b_fault = None
			if get_config(getRoom(jid),'bomb_fault'):
				try: bfp = int(get_config(getRoom(jid),'bomb_fault_persent'))
				except: bfp = bomb_fault_persent
				if bfp < 0 or bfp > 100: bfp = bomb_fault_persent
				b_fault = random.randint(0,100) < bfp
			if b_fault: send_msg(type, jid, text, L('It\'s a lucky day for you! Bomb is fault! Right wide is %s') % bc[2])
			else:
				send_msg(type, jid, '', L('/me explode %s') % text)
				if get_config(getRoom(jid),'bomb_action') == 'kick': muc_role(type, jid, nick, '%s\n%s' % (text,get_config(getRoom(jid),'bomb_reason')), 'none')
			bomb_random_list[getRoom(jid)] = get_next_random(getRoom(jid))

def bomb_presence(room,jid,nick,type,mass):
	global bomb_current
	if not get_config(getRoom(room),'bomb'): return
	try: bc = bomb_current[getRoom(room)]
	except: return
	if nick != bc[0]: return
	if type == 'unavailable':
		bc = bomb_current.pop(getRoom(room))
		if mass[8]:
			sleep(1)
			boom_bomb(room,'groupchat',mass[8],bc[2],None)
			bomb_random_list[getRoom(room)] = get_next_random(getRoom(room))

def bomb_message(room,jid,nick,type,text):
	global bomb_current,bomb_random_list
	if not get_config(getRoom(room),'bomb'): return
	try: bc = bomb_current[getRoom(room)]
	except: return
	if nick != bc[0]: return
	if text.lower() not in bc[1]: return
	bomb_current.pop(getRoom(room))
	type = 'groupchat'
	if text.lower() == bc[2]: send_msg(type, room, nick, L('Bomb is deactivated! Congratulations!'))
	else: boom_bomb(room,type,nick,bc[2],True)
	bomb_random_list[getRoom(room)] = get_next_random(getRoom(room))

def bomb_random():
	global bomb_current,bomb_random_list
	bt = bomb_random_sleep
	while not game_over and bt > 0:
		sleep(1)
		bt -= 1
	while not game_over:
		ntime = time.time()
		for tmp in confbase:
			tconf = getRoom(tmp)
			try: bla = get_config(tconf,'bomb_random_active') and (ntime - bomb_last_activity[tconf]) < int(get_config(tconf,'bomb_random_active_timer'))
			except: bla = True
			if get_config(tconf,'bomb') and get_config(tconf,'bomb_random') and bla:
				try: bsets = bomb_random_list[tconf]
				except:
					bsets = ntime
					bomb_random_list[tconf] = bsets
				if bsets < ntime:
					bomb_joke('groupchat', tconf, '', '')
					bomb_random_list[tconf] = get_next_random(tconf)
		bt = bomb_random_timer_check_period
		while not game_over and bt > 0:
			sleep(1)
			bt -= 1

def bomb_message_active(room,jid,nick,type,mass):
	global bomb_last_activity
	if jid != 'None': bomb_last_activity[getRoom(room)] = int(time.time())
	
global execute, presence_control, message_control

presence_control = [bomb_presence]
message_control = [bomb_message,bomb_message_active]

execute = [(4, 'bomb', bomb_joke, 2, L('Take a bomb joke!'))]
