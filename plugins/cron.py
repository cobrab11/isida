#!/usr/bin/python
# -*- coding: utf -*-

cron_base = set_folder+u'cron.db'	# база заданий

# cron add timer hh:mm:ss [repeat hh:mm:ss] command
# cron add alarm YYYY-MM-DD hh:mm:ss [tz [+|-]hh:mm] [repeat hh:mm:ss] command

def time_cron(type, jid, nick, text):
	ar = text.lower().split(' ',1)
	if ar[0] == 'show': msg = time_cron_show(ar[1])
	elif ar[0] == 'add': msg = time_cron_add(ar[1])
	elif ar[0] == 'del': msg = time_cron_del(ar[1])
	else: msg = L('What?')
	send_msg(type, jid, nick, msg)

# room t|a time True|None command

def time_cron_show(ar): return L('I can\'t!')

def time_cron_add_timer(ar): return L('I can\'t!')
	
def time_cron_add_alarm(ar): return L('I can\'t!')
	
def time_cron_add(ar):
	if ar[:5] == 'timer': return time_cron_add_timer(ar[5:])
	if ar[:5] == 'alarm': return time_cron_add_alarm(ar[5:])
	return L('Error!')
	
def time_cron_del(ar): return L('I can\'t!')

def cron_action():
	return

global execute, timer

timer = [cron_action]

execute = [(2, 'cron', time_cron, 2, '...')]
