#!/usr/bin/python
# -*- coding: utf -*-

logdir = 'logs_directory.txt'
if os.path.isfile(logdir): log_folder = readfile(logdir)
else: log_folder = 'logs/'
public_log = log_folder+'chatlogs'
system_log = log_folder+'syslogs'
if not os.path.exists(log_folder): os.mkdir(log_folder)
if not os.path.exists(public_log): os.mkdir(public_log)
if not os.path.exists(system_log): os.mkdir(system_log)

log_conf = set_folder+'logroom.db'
log_header ='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>\n'

def append_message_to_log(room,jid,nick,type,text):
	global public_log, system_log
	hr = getFile(log_conf,[])
	if len(hr) and room in hr:
		text,jid,nick = html_escape(text).replace('\n','<br>'), html_escape(jid), html_escape(nick)
		if type == 'groupchat' and text != 'None': msg_logger(room,jid,nick,type,text,public_log)
		if type == 'chat' and text != 'None': nick = 'chat | '+nick
		if text != 'None': msg_logger(room,jid,nick,type,text,system_log)

def msg_logger(room,jid,nick,type,text,logfile):
	lt = tuple(time.localtime())
	curr_path = logfile+'/'+room
	if not os.path.exists(curr_path): os.mkdir(curr_path)
	curr_path = curr_path+'/'+str(lt[0])
	if not os.path.exists(curr_path): os.mkdir(curr_path)
	curr_path += '/'+tZ(lt[1])
	if not os.path.exists(curr_path): os.mkdir(curr_path)
	curr_file = curr_path + '/'+tZ(lt[2])+'.html'
	log_body = '<a><font color=gray>['+onlytimeadd(tuple(localtime()))+']</font> '
	if nick == '': log_body += '<font color=#a00000>'+text+'</font></a><br>'
	else:
		if text[:4] == '/me ': log_body += '<font color=#0000a0>*'+nick+'</font><font color=#000000> '+text[4:]+'</font></a><br>\n'
		else: log_body += '<font color=#0000a0>&lt;'+nick+'&gt;</font><font color=#000000> '+text+'</font></a><br>\n'
	lht = room+' - '+str(lt[0])+'/'+tZ(lt[1])+'/'+tZ(lt[2])
	log_he = log_header +lht+'</title></head><body><p align="right"><font size=small><a href="http://isida-bot.com">http://isida-bot.com</a></font></p><h1>'+lht+'</h1><hr>\n'
	if not os.path.isfile(curr_file):
		fl = open(curr_file, 'a')
		fl.write(log_he.encode('utf-8'))
		fl.write(log_body.encode('utf-8'))
	else:
		fl = open(curr_file, 'a')
		fl.write(log_body.encode('utf-8'))
	ender = '</body></html>'
	fl.close()

def append_presence_to_log(room,jid,nick,type,mass):
	global public_log, system_log
	hr = getFile(log_conf,[])
	if len(hr) and room in hr:
		jid,nick = html_escape(jid), html_escape(nick)
		presence_logger(room,jid,nick,type,mass,0,public_log)
		presence_logger(room,jid,nick,type,mass,1,system_log)

def presence_logger(room,jid,nick,type,mass,mode,logfile):
	role,affiliation = html_escape(mass[1]), html_escape(mass[2])
	if nick[:11] != '<temporary>' and role != 'None' and affiliation != 'None':
		text,exit_type = html_escape(mass[0]).replace('\n','<br>'),mass[3]
		exit_message,show = html_escape(mass[4]), html_escape(mass[5])
		priority,not_found = mass[6],mass[7]
		lt = tuple(time.localtime())
		curr_path = logfile+'/'+room
		if not os.path.exists(curr_path): os.mkdir(curr_path)
		curr_path = curr_path+'/'+str(lt[0])
		if not os.path.exists(curr_path): os.mkdir(curr_path)
		curr_path += '/'+tZ(lt[1])
		if not os.path.exists(curr_path): os.mkdir(curr_path)
		curr_file = curr_path + '/'+tZ(lt[2])+'.html'
		log_body = '<a><font color=gray>['+onlytimeadd(tuple(localtime()))+']</font><i> '
		if type == 'unavailable': 
			log_body += '<font color=#00a000>'+nick
			if mode and jid != 'None': log_body += ' ('+jid+')'
			if len(exit_type): log_body += ' '+exit_type.lower()
			else: log_body += ' '+L('leave')
			if exit_message != '': log_body += ' ('+exit_message+') '
			log_body += '</font></i></a><br>\n'
		else:
			log_body += '<font color=#00a000>'+nick
			if not_found == 0:
				if mode and jid != 'None': log_body += ' ('+jid+')'
				log_body += ' '+L('join as')+' '+role+'/'+affiliation
			elif not_found == 1: log_body += ' '+L('now is')+' '+role+'/'+affiliation
			elif not_found == 2: log_body += ' '+L('now is')+' '
			if not_found == 0 or not_found == 2:
				if show != 'None': log_body += ' '+show
				else: log_body += ' online'
				if priority != 'None': log_body += ' ['+priority+']'
				else:  log_body += ' [0]'
				if text != 'None':  log_body += ' ('+text+')'
			log_body += '</font></i></a><br>\n'
		lht = room+' - '+str(lt[0])+'/'+tZ(lt[1])+'/'+tZ(lt[2])
		log_he = log_header +lht+'</title></head><body><p align="right"><font size=small><a href="http://isida-bot.com">http://isida-bot.com</a></font></p><h1>'+lht+'</h1><hr>\n'
		if not os.path.isfile(curr_file):
			fl = open(curr_file, 'a')
			fl.write(log_he.encode('utf-8'))
			fl.write(log_body.encode('utf-8'))
		else:
			fl = open(curr_file, 'a')
			fl.write(log_body.encode('utf-8'))
		ender = '</body></html>'
		fl.close()

global execute

message_control = [append_message_to_log]
presence_control = [append_presence_to_log]

def log_room(type, jid, nick, text):
	if type == 'groupchat': msg = L('This command aviable only in private!')
	else:
		hmode = text.split(' ')[0]
		try: hroom = text.split(' ')[1]
		except: hroom = jid
		hr = getFile(log_conf,[])
		if hmode == 'show':
			if len(hr):
				msg = L('Logged conferences:')
				for tmp in hr: msg += '\n'+tmp
			else: msg = L('Logs are turned off in all conferences.')
		elif hmode == 'add':
			if not match_room(hroom): msg = L('I am not in the %s') % hroom
			elif hr.count(hroom): msg = L('Logs for %s already enabled.') % hroom
			else:
				hr.append(hroom)
				msg = L('Logs for %s enabled.') % hroom
				writefile(log_conf,str(hr))
		elif hmode == 'del':
			if not match_room(hroom): msg = L('I am not in the %s') % hroom
			elif hr.count(hroom):
				hr.remove(hroom)
				msg = L('Logs for %s disabled.') % hroom
				writefile(log_conf,str(hr))
		else: msg = L('What?')
	send_msg(type, jid, nick, msg)

global execute

execute = [(2, 'log', log_room, 2, L('Logging history conference.\nlog [add|del|show][ room@conference.server.tld]'))]
