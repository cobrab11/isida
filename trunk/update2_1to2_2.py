# -*- coding: utf-8 -*- 

import os

update = '''
# --------------- Новое в версии 2.20 -----------------
ddos_limit = [1800,1800,1800,1800,1800,600,300,150,60,0]					# Время игнора при ddos'е в зависимости от уровня доступа
ddos_diff = [30,30,30,30,20,20,15,10,5,0]							# Промежуток между сообщениями для включения анти-ddos
amsg_limit = [86400,86400,86400,86400,86400,86400,43200,3600,1800,60]		# лимит времени следующей посылки сообщения для команды msgtoadmin
karma_timeout = [86400,86400,86400,86400,86400,86400,43200,3600,1800,5]	# время, через которое можно менять карму в зависимости от уровня доступа

#proxy = {'host':'localhost','port':3128,'user':'me','password':'secret'}	# Прокси
#proxy = {'host':'127.0.0.1','port':3128,'user':'','password':''}
#proxy = {'host':'localhost','port':3128}
#server = ('allports.jabber.ru', 443)										# Подключение минуя ресольвер
#secure = True																# Включение ssl/tls

# --- Опции для поддержки muc-filter --- Работает в тестовом режиме!!! ---
censor_text = '[censored]'			# Текст для закрытия мата
adblock_regexp = [u'([-0-9a-zA-Zа-яА-Я_+]+@c[-0-9a-zA-Z-.]+)', # Регекспы для блокиратора рекламы
				  u'зайди.*? .*?конф.*? .*?([-0-9a-zA-Zа-яА-Я_+]+@?)',
				  u'заходи.*? .*?конф.*? .*?([-0-9a-zA-Zа-яА-Я_+]+@?)',
				  u'зайди.*? .*?в.*? .*?([-0-9a-zA-Zа-яА-Я_+]+@?)',
				  u'заходи.*? .*?в.*? .*?([-0-9a-zA-Zа-яА-Я_+]+@?)',
				  u'конф.*? .*?([-0-9a-zA-Zа-яА-Я_+]+@?).*?зайди',
				  u'конф.*? .*?([-0-9a-zA-Zа-яА-Я_+]+@?).*?заходи'
				  u'все.*? .*?в.*? .*?([-0-9a-zA-Zа-яА-Я_+]+@?)']
muc_filter_large_message_size = 512 # Размер сообщения для фильтра

pastepath = 'paste/'						# Путь для больших сообщений
pasteurl  = 'http://isida-bot.com/paste/'	# Url для сообщений
html_paste_enable = True					# Тип True = html, False = text
paste_css_path = '.css/isida.css'			# Путь к css

muc_filter_match_count = 3					# счётчик одинаковых слов
muc_filter_match_warning_match = 3			# привышение одинаковых слов
muc_filter_match_warning_space = 5			# привышение пустых частей
muc_filter_match_warning_nn = 3				# количество переводов строк
muc_filter_match_view = 512					# лимит размера сообщения на отработку

paranoia_mode = False
'''

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

print 'Updater for Isida Jabber Bot from 2.10 to 2.20'
print '(c) Disabler Production Lab.'

config_path = 'settings/config.py'

tmp = readfile(config_path)
writefile(config_path,tmp+update)

print 'done!'
