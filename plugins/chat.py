#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSW_PREV = {}

MIND_FILE = set_folder + 'mind.txt'
EMPTY_FILE = set_folder + 'empty.txt'
ANSWER_FILE = set_folder + 'answer.txt'

list_of_mind = [m.strip() for m in readfile(MIND_FILE).split('\n') if m.strip()]
list_of_answers = readfile(ANSWER_FILE).split('\n')
list_of_empty = readfile(EMPTY_FILE).split('\n')

def flood_actions(type, room, nick, answ, msg):
	text = ''
	jid = getRoom(get_level(room,nick)[1])
	cof = getFile(conoff,[])
	tmppos = arr_semi_find(confbase, room)
	nowname = getResourse(confbase[tmppos])
	access_mode = get_level(room,nick)[0]
	if (room, answ[1:]) in cof: return
	if answ == '@ping':
		nicks = [d[1] for d in megabase if d[0]==room]
		tmp = [n for n in nicks if n.upper() in msg]
		if not tmp: text = 'ping'
		elif len(tmp) == 1: text = 'ping %s' % tmp[0]
		else: send_msg(type, room, nick, L('What?'))
	elif answ == '@anek': text = 'anek'
	elif answ == '@calend':
		if u'ЗАВТРА' in msg: text = 'calend %s.%s' % (time.gmtime()[1]+1, time.gmtime()[2])
		else: text = 'calend'
	if text: com_parser(access_mode, nowname, type, room, nick, text, jid)

def addAnswerToBase(tx):
	if not len(tx) or tx.count(' ') == len(tx): return
	mdb = sqlite3.connect(answersbase,timeout=base_timeout)
	answers = mdb.cursor()
	answers.execute('insert into answer values (?,?)', (len(answers.execute('select ind from answer').fetchall())+1,tx))
	mdb.commit()
	mdb.close()

def getRandomAnswer(tx):
	if not tx.strip(): return None
	mdb = sqlite3.connect(answersbase,timeout=base_timeout)
	answers = mdb.cursor()
	mrand = str(randint(1,len(answers.execute('select ind from answer').fetchall())))
	answ = to_censore(answers.execute('select body from answer where ind=?', (mrand,)).fetchone()[0])
	mdb.close()
	return answ

def getSmartAnswer(type, room, nick, text):
	if '?' in text: answ = random.choice(list_of_answers).strip()
	else: answ = random.choice(list_of_empty).strip()
	score,sc, var = 1.0,0,[answ]
	text = text.upper()
	for answer in list_of_mind:
		s = answer.split('||')
		sc = rating(s[0], text, room)
		if sc > score: score,var = sc,s[1].split('|')
		elif sc == score: var += s[1].split('|')
	answ = random.choice(var).decode('utf-8')
	if answ[0] != '@': return answ
	else:
		flood_actions(type, room, nick, answ, text)
		return ''

def rating(s, text, room):
	r,s = 0.0,s.decode('utf-8').split('|')
	for _ in s:
		if _ in text: r += 1
		if _ in ANSW_PREV.get(room, ''): r += 0.5	
	return r

def getAnswer(type, room, nick, text):
	text = text.strip()
	if get_config(getRoom(room),'flood') in ['random',True]: answ = getRandomAnswer(text)
	else:
		answ = getSmartAnswer(type, room, nick, text)
		ANSW_PREV[room] = text.upper()
	if type == 'groupchat' and text == to_censore(text): addAnswerToBase(text)
	return answ

global execute

execute = []
