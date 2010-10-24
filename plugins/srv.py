#!/usr/bin/python
# -*- coding: utf -*-

def srv_nslookup(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'nslookup '+text)

def srv_dig(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'dig '+text)

def srv_host(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'host '+text)

def srv_raw_check(type, jid, nick, text):
	if text.count('&') or text.count(';'): msg = L('Unavailable!')
	else: msg = shell_execute(text)
	send_msg(type, jid, nick, msg)

def chkserver(type, jid, nick, text):
	for a in ':;&/|\\\n\t\r': text = text.replace(a,' ')
	t = re.findall('[-a-zA-Z0-9�-��-�._/?#=@%]+',text,re.S)
	if len(t) >= 2:
		port = []
		for a in t:
			if a.isdigit(): port.append(a)
		for a in port: t.remove(a)
		if len(t)==1 and len(port)>=1:
			msg = shell_execute('nmap %s -p%s -P0 -T5' % (t[0],','.join(port)))
			try: msg = '%s\n%s' % (t[0],reduce_spaces_all(re.findall('SERVICE(.*)Nmap',msg,re.S+re.U)[0][1:-2]))
			except: msg = '%s - %s' % (t[0],L('unknown'))
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
