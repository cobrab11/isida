#!/usr/bin/python
# -*- coding: utf -*-
from xmpp import *
from sys import argv
from time import sleep
from random import *
from sys import maxint
from time import *
from pdb import *
import os, xmpp, time, sys, time, pdb, urllib

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

lfrom = 32
lto = 128
botName = 'Isida-Bot'
f = urllib.urlopen('http://isida.googlecode.com/svn')
ff = f.read()
botVersion = '1.4'

ver_file = 'version'
if os.path.isfile(ver_file):
	bvers = str(readfile(ver_file))
	botVersion += '.' + bvers[:-1]

# --- load config.txt

if os.path.isfile('config.txt'):
        execfile('config.txt')
else:
        errorHandler(u'config.txt is missed.')

# --- check parameters

baseParameters = [name, domain, password, newBotJid, mainRes, SuperAdmin, defaultConf]

baseErrors = [u'name', u'domain', u'password', u'newBotJid', u'mainRes', u'SuperAdmin', u'defaultConf']

for baseCheck in range(0, len(baseParameters)):
        if baseParameters[baseCheck]=='':
                errorHandler(baseErrors[baseCheck]+u' is missed in config.txt')

god = SuperAdmin

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

#error handler
def errorHandler(text):
        print u'\n*** Error ***'
        print text
        print u'more info at http://isida.googlecode.com\n'
        exit (0)

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
        join(cl, conf)
        sleep(1)

#leave [conference/nick]
def leaveconf(conference, server):
	global dm
        node = unicode(JID(conference).getResource())
        domain = server
        jid = JID(node=node, domain=server)
	if dm:
		cl = Client(jid.getDomain(), debug=[])
	else:
		cl = Client(jid.getDomain())
        conf = unicode(JID(conference))
        leave(cl, conf)
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
        
def join(conn, conference):
    global psw
    j = Presence(conference)
    j.setTag('x', namespace=NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
    j.getTag('x').setTagData('password', psw)
    cl.send(j)

def leave(conn, conference):
    j = Presence(conference, 'unavailable')
    j.setTag('x', namespace=NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
    cl.send(j)

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

def iqCB(sess,iq):
        nick = iq.getFrom()
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


        if (text != 'None') and (len(text)>2) and ownerbase.count(nick):
                for parse in comms:
                        if text[:len(parse[0])] == parse[0] or (text[:len(name)] == name and text[len(name)+2:len(parse[0])+len(name)+2] == parse[0]):
                                if not parse[2]:
                                        parse[1](type, room, nick, parse[3:])
                                elif parse[2] == 1:
                                        parse[1](type, room, nick)
                                elif parse[2] == 2:
                                        parse[1](type, room, nick, text[len(parse[0])+1:])


def presenceCB(sess,mess):
	global jidbase

        jid=unicode(mess.getJid())

#	print jid
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
	confbase = [defaultConf]
	writefile(confs,str(confbase))

print u''
print u'\n*****************************************************************'
print u'*** '+botName+' version '+botVersion+' ('+botOs+') ***' 
print u'*****************************************************************'
print u'\n--------------= (c) 2oo9 Disabler Production Lab. =--------------\n'

node = unicode(name)
lastnick = name

jid = JID(node=node, domain=domain, resource=mainRes)

print u'bot jid: '+unicode(jid)

psw = u''

dm = 1

if dm:
	cl = Client(jid.getDomain(), debug=[])
else:
	cl = Client(jid.getDomain())
cl.connect()
print u'Connected'

if newBotJid:
        print u'New jid: '+unicode(jid.getNode())+'@'+unicode(domain)
        features.register(cl, domain, {'username':node, 'password':password})
        print u'Registered'

cl.auth(jid.getNode(), password, jid.getResource())
print u'Autheticated'
cl.RegisterHandler('message',messageCB)
cl.RegisterHandler('iq',iqCB)
cl.RegisterHandler('presence',presenceCB)

print u'Wait conference'
for tocon in confbase:
        baseArg = unicode(tocon)+u'/'+unicode(name)
        conf = JID(baseArg)
        print tocon
        join(cl, conf)

lastserver = getServer(confbase[0])

print u'Joined'
while 1:
        cl.Process(1)

