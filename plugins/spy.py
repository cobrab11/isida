#!/usr/bin/python
# -*- coding: utf -*-

spy_base = set_folder+u'spy.db'		# база слежения
spy_stat_time = int(time.time())	# время последнего сканирования
scan_time = 1800					# интервал сканирования
spy_action_time = 86400				# интервал реакции на сканирование

#conf hrs usrs msgs action
def spy_add(text):
	if text == '': return u'что добавить?'
	text = text.lower()
	sb = getFile(spy_base,[])
	sconf = text.split(' ')[0]
	try: saction = text.split(' ',1)[1]
	except: return u'не заданы параметры слежения'
	for tmp in saction.split(' '):
		if tmp[0] != u'u' and tmp[0] != u'm':
			return u'не указан критерий слежения'
		try: int(tmp[1:])
		except: return u'не верно задан цифровой параметр'
	cb = []
	for tmp in confbase:
		cb.append(getRoom(tmp))
	if not cb.count(sconf): return u'меня нет в конфе '+sconf
	msg = u'Добавлено: '+text
	for tmp in sb:
		if tmp[0] == sconf:
			sb.remove(tmp)
			msg = u'Обновлено: '+text
			break
	cnt = 0
	for mega in megabase:
		if mega[0] == sconf: cnt += 1
	sb.append((sconf,int(time.time()),cnt,0,saction))
	writefile(spy_base,str(sb))
	return msg
	
def spy_del(text):
	if text == '': return u'что удалить?'
	text = text.lower().split(' ')[0]
	sb = getFile(spy_base,[])
	msg = u'Не найдено: '+text
	for tmp in sb:
		if tmp[0] == text:
			sb.remove(tmp)
			msg = u'Удалено: '+text
			writefile(spy_base,str(sb))
			break
	return msg
	
def spy_show(text):
	sb = getFile(spy_base,[])
	if not len(sb): return u'база пуста'
	msg = u'Слежение за конференциями:'
	for tmp in sb:
		msg += u'\n'+tmp[0]+' '+tmp[4]+' ('+un_unix(int(time.time()-tmp[1]))+u'|u'+str(tmp[2])+u'|m'+str(tmp[3])+')'
	msg += u'\nСледующее сканирование через '+un_unix(int(scan_time-(time.time()-spy_stat_time)))
	return msg
	
def conf_spy(type, jid, nick,text):
	msg = None
	if text[:4] == 'add ': msg = spy_add(text[4:])
	elif text[:4] == 'del ': msg = spy_del(text[4:])
	elif text[:4] == 'show': msg = spy_show(text[4:])
	if not msg: msg = u'Курим помощь по команде!'
	send_msg(type, jid, nick, msg)

def spy_message(room,jid,nick,type,text):
	sb = getFile(spy_base,[])
	for tmp in sb:
		if tmp[0] == getRoom(room):
			ms = (tmp[0],tmp[1],tmp[2],tmp[3]+1,tmp[4])
			sb.remove(tmp)
			sb.append(ms)
			writefile(spy_base,str(sb))
			break

def get_spy_stat():
	global spy_stat_time
	if time.time()-spy_stat_time < scan_time: return None
	spy_stat_time = time.time()
	sb = getFile(spy_base,[])
	for tmp in sb:
		cnt = 0
		for mega in megabase:
			if mega[0] == tmp[0]:
				cnt += 1
		ms = (tmp[0],tmp[1],(tmp[2]+cnt)/2.0,tmp[3],tmp[4])
		sb.remove(tmp)
		sb.append(ms)
		writefile(spy_base,str(sb))

def spy_action():
	global confs, confbase
	if len(confbase) == 1: return None # Last conference
	sb = getFile(spy_base,[])
	for tmp in sb:
		if time.time()-tmp[1] > spy_action_time:
			act = tmp[4].split(' ')
			mist = None
			for tmp2 in act:
				if tmp2[0] == u'u' and int(tmp2[1:]) > tmp[2]: mist = tmp2
				elif tmp2[0] == u'm' and int(tmp2[1:]) > tmp[3]: mist = tmp2
				sb.remove(tmp)
				if mist:
					if arr_semi_find(confbase, tmp[0]) >= 0:
						confbase = arr_del_semi_find(confbase,tmp[0])
						writefile(confs,str(confbase))
						leaveconf(tmp[0], domain, u'Выхожу в связи с низкой активностью конференции')
						for tmpo in ownerbase: send_msg('chat', getRoom(tmpo), '', u'Конференция '+tmp[0]+u' покинута по условию spy плагина: '+mist)
				else: sb.append((tmp[0],int(time.time()),tmp[2], 0,tmp[4]))
				writefile(spy_base,str(sb))

global execute, timer, message_control

timer = [get_spy_stat, spy_action]

message_control = [spy_message]

execute = [(2, u'spy', conf_spy, 2, u'Проверка активности конференции\nspy add <conference>[ u<number>][ m<number>] - добавить конференцию в список мониторинга активности. u - среднее число участников, m - количество сообщение за сутки. При невыполнении хотябы одного условия - бот выйдет из конференции\nspy del <conference> - удалить конференцю из списка мониторинга\nspy show - показать активное слежение')]
