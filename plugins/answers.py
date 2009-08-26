#!/usr/bin/python
# -*- coding: utf -*-

answers_file = u'answers.txt'

def answers_ie(type, jid, nick, text):
	if text.lower().strip().split(' ',1)[0] == 'export':
		try: fname = text.lower().split(' ',1)[1]
		except: fname = answers_file
		mdb = sqlite3.connect(answersbase)
		cu = mdb.cursor()
		base_size = len(cu.execute('select * from answer').fetchall())
		fnd = cu.execute('select body from answer where body like ? group by body order by body',('%',)).fetchall()
		answer = ''
		msg = u'Экспорт в файл: '+fname+u' | Всего записей: '+str(base_size)+u' | После удаления дубликатов: '+str(len(fnd))
		for i in fnd:
			if i[0] != '': answer += i[0].strip() +'\n'
		writefile(fname,answer.encode('utf-8'))
	elif text.lower().strip().split(' ',1)[0] == 'import':
		try: fname = text.lower().split(' ',1)[1]
		except: fname = answers_file
		if os.path.isfile(fname):
			answer = readfile(fname).decode('utf-8')
			answer = answer.split('\n')
			mdb = sqlite3.connect(answersbase)
			cu = mdb.cursor()
			cu.execute('delete from answer where body like ?',('%',))
			msg = u'Импорт из файла: '+fname+u' | Всего записей: '+str(len(answer))
			idx = 1
			for i in answer:
				if i != '':
					cu.execute('insert into answer values (?,?)', (idx,unicode(i.strip())))
					idx += 1
			mdb.commit()
		else: msg = u'Не найден файл ответов '+fname
	else: msg = u'Не указан параметр export/import'
	send_msg(type, jid, nick, msg)

global execute

execute = [(2, u'answers', answers_ie, 2, u'Импорт/Экспорт базы ответов в текстовый файл.\nanswers import [название файла] - импорт ответов из текстового файла в базу\nanswers export [название файла] - экспорт ответов из базы в текстовый файл')]
