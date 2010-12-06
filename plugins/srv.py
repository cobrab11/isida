#!/usr/bin/python
# -*- coding: utf-8 -*-

def srv_nslookup(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'nslookup '+text)

def srv_dig(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'dig '+text)

def srv_host(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'host '+text)

def srv_raw_check(type, jid, nick, text):
	text = ' '.join(tuple(re.findall(u'[-a-zA-Z0-9а-яА-Я._?#=@%]+',text,re.S)))
	print text
	send_msg(type, jid, nick, shell_execute(text))

def chkserver(type, jid, nick, text):
	for a in ':;&/|\\\n\t\r': text = text.replace(a,' ')
	t = re.findall(u'[-a-zA-Z0-9а-яА-Я._?#=@%]+',text,re.S)
	if len(t) >= 2:
		port = []
		for a in t:
			if a.isdigit(): port.append(a)
		for a in port: t.remove(a)
		if len(t)==1 and len(port)>=1:
			t = t[0]
			port.sort()
			msg = shell_execute('nmap %s -p%s -P0 -T5' % (t,','.join(port)))
			try: msg = '%s\n%s' % (t,reduce_spaces_all(re.findall('SERVICE(.*)Nmap',msg,re.S+re.U)[0][1:-2]))
			except:
				try:
					msg = ''
					for a in port:
						sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
						try:
							sock.connect((t,int(a)))
							s = L('on')
						except: s = L('off')
						msg += '\n%s %s' % (a,s)
						sock.close()
					msg = '%s%s' % (t,msg)
				except: msg = '%s - %s' % (t,L('unknown'))
			msg = L('Port status at %s') % msg
		else: msg = L('What?')
	else: msg = L('What?')
	send_msg(type, jid, nick, msg)

global execute

if not paranoia_mode: execute = [(6, 'nslookup', srv_nslookup, 2, L('Command nslookup')),
		   (6, 'host', srv_host, 2, L('Command host')),
		   (6, 'dig', srv_dig, 2, L('Command dig')),
		   (4, 'port', chkserver, 2, L('Check port activity\nport server port1 [port2 ...]'))]
else: execute = []
