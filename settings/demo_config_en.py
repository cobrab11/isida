# -*- coding: utf-8 -*- 

#------------------------------------------------
#             Isida-bot Config file
#                    v1.4en
#------------------------------------------------

Settings = {
'nickname': 		u'<write here bot nick>',					# bot nick in conferences
'jid':				u'isida-jabber-bot@domain.tld/isida-bot',	# bot jid
'password':			u'********',								# password
'status':			u'online',									# bot status chat|online|away|xa|dnd
'priority':			0,											# priority
'message':			u'Йа аццкое железко!'}						# status-message

SuperAdmin 		=	u'aaa@bbb.ru'								# bot owner jid
defaultConf		=	u'isida@conference.jabber.ru'				# start conference
prefix			=	u'_'										# command prefix
msg_limit		= 	2048										# limit of the size of messages

#ignore_owner	=	True										# don't allow execute offered commands for bot owner
#debugmode		=	True										# mode _not_to_ignore_an_error_
#dm				=	True										# debugging mode xmpppy
#dm2			=	True										# mode of show of operations of a bot in console
CommandsLog		=	True										# logging commands of a bot
#thread_type	=	None										# threads type thread/threading. default - threading

# --- Файлы ---
slog_folder = 'log/'					# папка системных логов
set_folder 	= 'settings/'				# папка настроек
back_folder = 'backup/'					# папка хранения резервных копий
loc_folder 	= 'locales/'				# папка локализаций
log_folder 	= 'logs/'					# папка логов конференций
LOG_FILENAME = slog_folder+'error.txt'	# логи ошибок
c_file = set_folder+'conference.config' # конфиг конференции
ver_file = set_folder+'version'			# версия бота
alfile = set_folder+'aliases'			# сокращения
owners = set_folder+'owner'				# база владельцев
ignores = set_folder+'ignore'			# черный список
confs = set_folder+'conf'				# список активных конф
feeds = set_folder+'feed'				# список rss каналов + md5 последниx новостей по каждому каналу
cens = set_folder+'censor.txt'			# список "запрещенных" слов для болтуна
conoff = set_folder+'commonoff'			# список "запрещенных" команд для бота
saytobase = set_folder+'sayto.db'		# база команды "передать"
agestatbase = set_folder+'agestat.db'	# статистика возрастов
talkersbase = set_folder+'talkers.db'	# статистика болтунов
wtfbase = set_folder+'wtfbase2.db'		# определения
answersbase = set_folder+'answers.db'	# ответы бота
scrobblebase = set_folder+'scrobble.db'	# база PEP скробблера
loc_file = set_folder+'locale'			# файл локализации
time_limit_base = set_folder+'saytoowner.db'	# файл ограничений команды msgtoadmin
wzbase = set_folder+'wz.db'				# база кодов для команд wz*
gisbase = set_folder+'gis.db'			# база кодов для команд gis*
hide_conf = set_folder+'hidenroom.db'	# файл скрытых конференций
jid_base = set_folder+'jidbase.db'		# статистика jid'ов
top_base = set_folder+'topbase.db'		# активность конференции
blacklist_base = set_folder + 'blacklist.db'	# черный список конференций
karmabase = set_folder+'karma.db'		# база кармы
log_conf = set_folder+'logroom.db'		# список конференций с логами
tban = set_folder+'temporary.ban'		# лог временного бана
af_alist = set_folder+'alist.aff'		# alist аффиляций
ro_alist = set_folder+'alist.rol'		# alist ролей
ignoreban = set_folder+'ignoreban.db'	# список игнора при глобальном бане
spy_base = set_folder+'spy.db'			# база слежения
public_log = log_folder+'chatlogs'		# папка для записи публичных логов конференций
system_log = log_folder+'syslogs'		# папка для записи системных логов конференций
logs_css_path = '../../../.css/isida.css'	# путь к css файлу для логов
tld_list = 'tld/tld.list'				# список tld кодов
poke_file = 'plugins/poke.txt'			# список ответов для команды poke
answers_file = 'answers.txt'			# имя файла по умолчанию для импорта/экспорта ответов
date_file = 'plugins/date.txt'			# список праздников


# --- Переменные ---
syslogs_enable = True				# Включение системных логов
status_logs_enable = True			# Запись в логи смены статусов
aff_role_logs_enable = True			# Запись в логи смены аффиляций и ролей
html_logs_enable = True				# Тип логов True = html, False = text
karma_limit = 5						# минимальная карма при которой изменение доступно не постоянным участникам
karma_show_default_limit = 10		# количество участников по умолчанию для команды karma top+/-
karma_show_max_limit = 20			# максимальное количество участников для команды karma top+/-
watch_size = 900					# период запросов в секундах для плагина watcher
user_agent = 'Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'	# user agent для большинства web запросов
size_overflow = 262144				# лимит страницы в байтах для команды www.
youtube_max_videos 		= 10		# максимальное количество ссылок при показе
youtube_default_videos 	= 3			# количество ссылок по умолчанию
youtube_max_page_size 	= 131072	# лимит размера страницы при загрузке
youtube_default_lang 	= 'ru'		# язык по умолчанию
age_default_limit = 10				# количество участников по умолчанию для команд плагина age
age_max_limit = 100					# максимальное количество участников для команд плагина age
anek_private_limit = 500			# размер, свыше которого анекдот будет посылаться в приват
troll_default_limit = 10			# Количество сообщений для команды troll
troll_max_limit = 100				# Максимальное количество сообщений для команды troll
troll_sleep_time = 0.05				# Задержка отправки сообщений для команды troll
backup_sleep_time = 0.1				# Задержки при запросах команды backup
calendar_default_splitter = '_'		# Разделитель по умолчанию для календаря
clear_delay = 1.3					# Задержка между сообщениями при команде clear
clear_default_count = 20			# Количество сообщений для команды clear
clear_max_count = 100				# Максимальное количество сообщений для команды clear
inlist_sleep_time = 0.1				# Время проверки ответов на запросы плагина inlist
ping_type = NS_VERSION				# Тип iq запроса для пинга
ping_digits = 3						# Количество знаков после запятой при пинге
lfm_api = 'xxxxxxxxxxxxxxxx'		# Api для работы плагина lastfm
lastfm_max_limit = 10				# Количество ответов для команд плагина lastfm
reboot_time = 180					# Таймаут рестарта бота при ошибке не стадии подключения (нет инета, ошибка авторизации)
timeout = 600						# Таймаут в секундах на iq запросы
schedule_time = 10					# Время проверки расписания
sayto_timeout = 1209600				# Время жизни сообщения, которое бот не смог передать по команде sayto
sayto_cleanup_time = 86400			# Время через которое производятся зачистки sayto базы
scan_time = 1800					# Интервал сканирования для команды spy
spy_action_time = 86400				# Интервал реакции на сканирование для команды spy
torrent_default_count = 3			# Количество ответов для команды torrent
rss_max_feed_limit = 10				# Максимальное количество новостей
rss_min_time_limit = 10				# Минимальное время проверки rss в минутах
default_msg_limit = msg_limit		# Размер сообщений по умолчанию
pep_scrobbler_max_count = 10		# Максимальное количество ответов для pep скробблера
whereis_timeout = 10				# Таймаут ожидания ответа для команды whereis
whereis_time_dec = 0.1				# Частота проверки ответа для команды whereis
disco_max_limit = 10				# Максимальное количество ответов для команды disco
juick_user_post_limit = 3			# Количество постов при запросе по пользователю
juick_user_post_size = 50			# Количество символов в посте при запросе по пользователю
juick_tag_user_limit = 5			# Количество пользователей при запросе по тегу
juick_tag_user_max = 20				# Максимальное количество пользователей при запросе по тегу
juick_msg_answers_default = 0		# Количество ответов при запросе но номеру сообщения
juick_tag_post_limit = 3			# Количество постов при запросе по тегу
juick_tag_post_size = 120			# Количество символов в посте при запросе по тегу
iq_time_enable = True				# Разрешение отвечать на запрос времени бота
iq_uptime_enable = True				# Разрешение отвечать на запрос аптайма бота
iq_version_enable = True			# Разрешение отвечать на запрос версии бота

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
muc_filter_match_warning_space = 5			# превышение количества пустых частей
muc_filter_match_warning_space = 5			# прeвышение пустых частей
muc_filter_match_view = 512					# лимит размера сообщения на отработку

muc_filter_match_warning_nn = 3				# количество переводов строк