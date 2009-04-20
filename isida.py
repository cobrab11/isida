#!/usr/bin/python
# -*- coding: utf -*-
from xmpp import *
from sys import argv
from time import sleep
from random import *
from sys import maxint
from time import *
from pdb import *
import os, xmpp, time, sys, time, pdb, urllib, re

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

def parser(text):
        text = unicode(text)
        ttext = u''
        i = 0
        while i<len(text):
                if (text[i]<='~'): # or (text[i]>=u'А' and text[i]<=u'я'):
                        ttext+=text[i]
                else:
                        ttext+='?'
                i=i+1
        ttext = unicode(ttext)
        return ttext

def tZ(val):
	rval = str(val)
        if val<10:
		rval = '0'+rval
	return rval

def timeadd():
	lt = localtime()
	st = tZ(lt[2])+u'.'+tZ(lt[1])+u'.'+tZ(lt[0])+u' '+tZ(lt[3])+u':'+tZ(lt[4])+u':'+tZ(lt[5])
	return st

def pprint(text):
	print parser('['+timeadd()+'] '+text)

def send_presence_all(sm):
	for tocon in confbase:
		baseArg = unicode(tocon)
		if not tocon.count('/'):
		        baseArg += u'/'+unicode(name)
	        conf = JID(baseArg)
	        leave(conf,sm)
	        pprint('leave: '+tocon)

#error handler
def errorHandler(text):
        pprint(u'\n*** Error ***')
        pprint(text)
        pprint(u'more info at http://isida.googlecode.com\n')
        exit (0)

lfrom = 32
lto = 128
botName = 'Isida-Bot'
f = urllib.urlopen('http://isida.googlecode.com/svn')
ff = f.read()
botVersion = '1.4'
capsVersion = botVersion

ver_file = 'version'
if os.path.isfile(ver_file):
	bvers = str(readfile(ver_file))
	botVersion += '.' + bvers[:-1]

# --- load config.txt

configname = u'config.py'

if os.path.isfile(configname):
        execfile(configname)
else:
        errorHandler(configname+u' is missed.')

capsNode = 'http://isida.googlecode.com'

# --- check parameters

baseParameters = [name, domain, password, newBotJid, mainRes, SuperAdmin, defaultConf, CommStatus, StatusMessage, Priority]

baseErrors = [u'name', u'domain', u'password', u'newBotJid', u'mainRes', u'SuperAdmin', u'defaultConf', u'CommStatus', u'StatusMessage', u'Priority']

megabase = []

# --- subs ----

for baseCheck in range(0, len(baseParameters)):
        if baseParameters[baseCheck]=='':
                errorHandler(baseErrors[baseCheck]+u' is missed in '+configname)

god = SuperAdmin

def arr_semi_find(array, string):
	astring = [unicode(string)]
	position = -1
	for arr in array:
#		print re.findall(string, arr), astring
		if re.findall(string, arr) == astring:
			position = array.index(arr)
#	print position
	return position

def arr_del_by_pos(array, position):
	return array[:position] + array[position+1:]

def arr_del_semi_find(array, string):
	pos = arr_semi_find(array, string)
	if pos >= 0:
		array = arr_del_by_pos(array,pos)
	return array

# upload addons
execfile('main.py')

def send_msg(mtype, mjid, mnick, mmessage):
        if mtype == 'groupchat':
                mmessage = mnick+': '+mmessage
        else:
                mjid += '/' + mnick
        cl.send(xmpp.Message(mjid, mmessage, mtype))

def os_version():
	jSys = sys.platform
	jOs = os.name
	japytPyVer = sys.version
	japytPyVer = japytPyVer.split(',')
	japytPyVer = japytPyVer[0]+')'

	if jOs == u'posix':
	        osInfo = os.uname()
		if osInfo[4].count('iPhone'):
			if osInfo[4].count('iPhone1,1'):
				japytOs = 'iPhone 2G'
			elif osInfo[4].count('iPhone1,2'):
				japytOs = 'iPhone 3G'
			else:
				japytOs = 'iPhone Unknown (platform: '+osInfo[4]+')'

			if osInfo[3].count('1228.7.37'):
				japytOs += ' FW.2.2.1'
			elif osInfo[3].count('1228.7.36'):
				japytOs += ' FW.2.2'
			else:
				japytOs += ' FW.Unknown ('+osInfo[3]+')'


			japytOs += ' ('+osInfo[1]+') / Python v'+japytPyVer
		else:
		        japytOs = osInfo[0]+' ('+osInfo[2]+'-'+osInfo[4]+') / Python v'+japytPyVer

	elif jSys == 'win32':
	        def get_registry_value(key, subkey, value):
	            import _winreg
	            key = getattr(_winreg, key)
	            handle = _winreg.OpenKey(key, subkey)
	            (value, type) = _winreg.QueryValueEx(handle, value)
	            return value
	        def get(key):
	            return get_registry_value(
	                "HKEY_LOCAL_MACHINE", 
	                "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
	                key)
	        osInfo = get("ProductName")
	        spInfo = get("CSDVersion")
	        buildInfo = get("CurrentBuildNumber")
	        japytOs = osInfo+' '+spInfo+' (Build: '+buildInfo+') / Python v'+japytPyVer
	else:
	        japytOs = 'unknown'
	return japytOs

botOs = os_version()

#join [conference/nick]
def joinconf(conference, server):
        global mainRes, dm
        node = unicode(JID(conference).getResource())
        domain = server
        jid = JID(node=node, domain=server, resource=mainRes)
	if dm:
		cl = Client(jid.getDomain(), debug=[])
	else:
		cl = Client(jid.getDomain())
        conf = unicode(JID(conference))
        join(conf)
        sleep(1)

#leave [conference/nick]
def leaveconf(conference, server, sm):
	global dm
        node = unicode(JID(conference).getResource())
        domain = server
        jid = JID(node=node, domain=server)
	if dm:
		cl = Client(jid.getDomain(), debug=[])
	else:
		cl = Client(jid.getDomain())
        conf = unicode(JID(conference))
        leave(conf, sm)
        sleep(1)

#---------------------------------------

def get_space(text):
        lenrig = len(text)
        i = 1
        spc = 0
        while (i<lenrig):
                if (text[i]==" "):
                        spc=spc+1
                i=i+1
        return spc
        
def join(conference):
    j = Presence(conference, show=CommStatus, status=StatusMessage, priority=Priority)
    j.setTag('x', namespace=NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
    j.getTag('x').setTagData('password', psw)
    j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
    cl.send(j)

def leave(conference, sm):
    j = Presence(conference, 'unavailable', status=sm)
    j.setTag('x', namespace=NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
    j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
    cl.send(j)

def iqCB(sess,iq):
        nick = iq.getFrom()
	pprint(u' *** iq:version from '+unicode(nick))
        id = iq.getID()
        if iq.getType()=='get':
                if iq.getTag(name='query', namespace=xmpp.NS_VERSION):
                        i=xmpp.Iq(to=nick, typ='result')
                        i.setAttr(key='id', val=id)
                        i.setQueryNS(namespace=xmpp.NS_VERSION)
                        i.getTag('query').setTagData(tag='name', val=botName)
                        i.getTag('query').setTagData(tag='version', val=botVersion)
                        i.getTag('query').setTagData(tag='os', val=botOs)
                        cl.send(i)


def messageCB(sess,mess):
        global otakeRes, mainRes, psw, lfrom, lto, jidbase, owners, ownerbase, confbase, confs, lastserver, lastnick, comms
        room=unicode(mess.getFrom().getStripped())
        nick=unicode(mess.getFrom().getResource())
        text=unicode(mess.getBody())
        type=unicode(mess.getType())
        towh=unicode(mess.getTo().getStripped())
	stamp=unicode(mess.getTimestamp())

#        print '---\n',parser(room), parser(nick), parser(text), parser(type), parser(towh), parser(stamp)

        rn = room+"/"+nick

        text=unicode(text)

# 0 - конфа # 1 - ник # 2 - роль # 3 - аффиляция # 4 - jid

	access_mode = 0
	jid = 'None'
	if nick != name:
		for base in megabase:
			if (base[1].count(nick) and base[0].lower()==room and (base[3]==u'admin' or base[3]==u'owner')):
				jid = base[4]
				access_mode = 1
				
	if ownerbase.count(getRoom(jid)):
		access_mode = 2

#	print access_mode, text

	tmppos = arr_semi_find(confbase, room)
	if tmppos == -1:
		nowname = name
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '':
			nowname = name

        if (text != 'None') and (len(text)>2):
                for parse in comms:
			if access_mode >= parse[0] and nick != nowname:
				if text[:len(nowname)] == nowname:
					text = text[len(nowname)+2:]

        	                if text[:len(parse[1])].lower() == parse[1].lower():
					pprint(jid+' '+room+'/'+nick+' ['+str(access_mode)+'] '+text)
        	                        if not parse[3]:
        	                                parse[2](type, room, nick, parse[4:])
        	                        elif parse[3] == 1:
        	                                parse[2](type, room, nick)
        	                        elif parse[3] == 2:
        	                                parse[2](type, room, nick, text[len(parse[1])+1:])


def presenceCB(sess,mess):
	global jidbase, megabase
        room=unicode(mess.getFrom().getStripped())
        nick=unicode(mess.getFrom().getResource())
        text=unicode(mess.getStatus())
        role=unicode(mess.getRole())
        affiliation=unicode(mess.getAffiliation())
        jid=unicode(mess.getJid())
        priority=unicode(mess.getPriority())
        show=unicode(mess.getShow())
        reason=unicode(mess.getReason())
        type=unicode(mess.getType())
        status=unicode(mess.getStatusCode())
        actor=unicode(mess.getActor())

	if type=='unavailable':
		if megabase.count([room, nick, role, affiliation, jid]):
			megabase.remove([room, nick, role, affiliation, jid])
	else:
		if not megabase.count([room, nick, role, affiliation, jid]):
			megabase.append([room, nick, role, affiliation, jid])

#        print room, nick, text, role, affiliation, jid, priority, show, reason, type, status, actor

	if not jidbase.count(jid) and jid != 'None':
		jidbase.append(jid)
		writefile(jidbasefile,str(jidbase))

def onoff(msg):
        if msg:
                return 'ON'
        else:
                return 'OFF'

def toSymbol(text,symbol):
        lt = len(text)
        i = 0
        while i<lt and text[i]!=symbol:
                i+=1
        return text[:i]

def toSymbolPosition(text,symbol):
        lt = len(text)
        i = 0
        while i<lt and text[i]!=symbol:
                i+=1
        if i==lt:
                i = -1
        return i

def toSymbolPositionBack(text,symbol):
        i = len(text)-1
        while i>0 and text[i]!=symbol:
                i-=1
        if i==0:
                i+=1
        return i

def getName(jid):
        return toSymbol(jid,'@')

def getServer(jid):
        lt = len(jid)
        i = 0
        server = ''
        while i<lt and jid[i]!='@':
                i+=1
        i+=1
        while i<lt and jid[i]!='/':
                server+=jid[i]
                i+=1
        return server

def getResourse(jid):
        lt = len(jid)
        i = 0
        while i<lt and jid[i]!='/':
                i+=1
        return jid[i+1:]

def getRoom(jid):
	return getName(jid)+'@'+getServer(jid)

def shelude():
	lt=localtime()
	l_hi = lt[0]*400+lt[1]*40+lt[2]
	l_lo = lt[3]*3600+lt[4]*60+lt[5]

	if os.path.isfile(feeds):
		feedbase = eval(readfile(feeds))
	else:
		feedbase = []
		writefile(feeds,str(feedbase))

	if os.path.isfile(lafeeds):
		lastfeeds = eval(readfile(lafeeds))
	else:
		lastfeeds = []
		writefile(lafeeds,str(lastfeeds))

	for fd in feedbase:
		ltime = fd[1]
		timetype = ltime[-1:].lower()
		if not (timetype == 'h' or timetype == 'm'):
			timetype = 'h'
		try:
			ofset = int(ltime[:-1])
		except:
			ofset = 4

		if timetype == 'h':
			ofset *= 3600
		elif timetype == 'm':
			ofset *= 60

		lttime = fd[3]
		ll_hi = lttime[0]*400+lttime[1]*40+lttime[2]
		ll_lo = lttime[3]*3600+lttime[4]*60+lttime[5]

		if ll_lo + ofset <= l_lo:
			pprint(u'check rss: '+fd[0]+u' in '+fd[4])
			type = 'groupchat'
			jid = fd[4]
			nick = 'RSS'
			text = 'now '+fd[0]+' 10 '+fd[2]
			rss(type, jid, nick, text)
			text = 'del '+fd[0]

			text = text.split(' ')
			link = text[1]
			if link[:7] != 'http://':
        		        link = 'http://'+link

			bedel = 0
			for rs in feedbase:
				if rs[0] == link and rs[4] == jid:
					feedbase.remove(rs)
					bedel = 1
			if bedel:
				writefile(feeds,str(feedbase))

			text = 'add '+fd[0]+' '+fd[1]+' '+fd[2]

			lt=localtime()
			text = text.split(' ')
			link = text[1]
			if link[:7] != 'http://':
        		        link = 'http://'+link
			feedbase.append([link, text[2], text[3], lt[:6], jid])
			writefile(feeds,str(feedbase))


# ---------- HERE WE GO!!! -----------

jidbasefile = 'jidbase'

if os.path.isfile(jidbasefile):
	jidbase = eval(readfile(jidbasefile))
else:
	jidbase = []
	writefile(jidbasefile,str(jidbase))

owners = 'owner'

if os.path.isfile(owners):
	ownerbase = eval(readfile(owners))
else:
	ownerbase = [god]
	writefile(owners,str(ownerbase))

confs = 'conf'

if os.path.isfile(confs):
	confbase = eval(readfile(confs))
else:
	confbase = [defaultConf+u'/'+name]
	writefile(confs,str(confbase))

pprint(u'****************************')
pprint(u'*** Bot Name: '+botName)
pprint(u'*** Version '+botVersion)
pprint(u'*** OS '+botOs)
pprint(u'******************************')
pprint(u'*** (c) 2oo9 Disabler Production Lab.')

node = unicode(name)
lastnick = name

jid = JID(node=node, domain=domain, resource=mainRes)

pprint(u'bot jid: '+unicode(jid))

psw = u''

dm = 1

if dm:
	cl = Client(jid.getDomain(), debug=[])
else:
	cl = Client(jid.getDomain())
cl.connect()
pprint(u'Connected')

if newBotJid:
        pprint(u'New jid: '+unicode(jid.getNode())+'@'+unicode(domain))
        features.register(cl, domain, {'username':node, 'password':password})
        pprint(u'Registered')

cl.auth(jid.getNode(), password, jid.getResource())
pprint(u'Autheticated')
cl.RegisterHandler('message',messageCB)
cl.RegisterHandler('iq',iqCB)
cl.RegisterHandler('presence',presenceCB)

pprint(u'Wait conference')
for tocon in confbase:
	baseArg = unicode(tocon)
	if not tocon.count('/'):
		baseArg += u'/'+unicode(name)
	conf = JID(baseArg)
	pprint(tocon)
	join(conf)

lastserver = getServer(confbase[0])

pprint(u'Joined')

while 1:
	try:
		while 1:
        		cl.Process(1)
			shelude()

	except KeyboardInterrupt:
		StatusMessage = 'Shut down by CTRL+C'
		pprint(StatusMessage)
		send_presence_all(StatusMessage)
		sleep(5)
		exit(0)
	except Exception, SM:
		lt = localtime()
		pprint('*** Error ***')
#		pprint(SM)
		raise



