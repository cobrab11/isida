#!/usr/bin/python
# -*- coding: utf -*-
from xmpp import *
from sys import argv
from random import *
from sys import maxint
from time import *
from pdb import *
import os, xmpp, time, sys, time, pdb, urllib, re, logging, thread, operator, sqlite3

LOG_FILENAME = u'log/error.txt'		# логи

set_folder = u'settings/'		# папка настроек

preffile = set_folder+u'prefix'		# префиксы
ver_file = set_folder+u'version'	# версия бота
configname = set_folder+u'config.py'	# конфиг бота
alfile = set_folder+u'aliases'		# сокращения
fld = set_folder+u'flood'		# автоответчик
sml = set_folder+u'smile'		# смайлы на роли
owners = set_folder+u'owner'		# база владельцев
ignores = set_folder+u'ignore'		# черный список
confs = set_folder+u'conf'		# список активных конф
tmpf = set_folder+u'tmp'		# флаг завершения бота
feeds = set_folder+u'feed'		# список rss каналов
lafeeds = set_folder+u'lastfeeds'	# последние новости по каждому каналу
cens = set_folder+u'censor.txt'     	# список "запрещенных" слов для болтуна

mainbase = set_folder+u'main.db'	# основная база данных

logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

global execute, prefix, comms

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

def untime(var):
	try:
		for vv in var:
			int(vv)
	except:
		var = var[var.index('(')+1:var.index(')')]
		var = var.split(',')
		stt = []
		for st in var:
			sttt = st.split('=')
			stt.append(int(sttt[1]))
		var = stt
	return var

def parser(text):
	logt=untime(localtime())
	logfile = 'log/'+tZ(logt[0])+tZ(logt[1])+tZ(logt[2])

	if os.path.isfile(logfile):
		log = eval(readfile(logfile))
	else:
		log = []
		writefile(logfile,str(log))

	log.append(text)
	writefile(logfile,str(log))

        text = unicode(text)
        ttext = u''
        i = 0
        while i<len(text):
                if (text[i]<='~'):# or (text[i]>=u'А' and text[i]<=u'я'):
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

def timeadd(lt):
	st = tZ(lt[2])+u'.'+tZ(lt[1])+u'.'+tZ(lt[0])+u' '+tZ(lt[3])+u':'+tZ(lt[4])+u':'+tZ(lt[5])
	return st

def pprint(text):
        text = text
	zz = parser('['+timeadd(untime(localtime()))+'] '+text)
#	print zz

def send_presence_all(sm):
	for tocon in confbase:
		baseArg = unicode(tocon)
		if not tocon.count('/'):
		        baseArg += u'/'+unicode(nickname)
	        conf = JID(baseArg)
	        leave(conf,sm)
		sleep(0.2)
	        pprint('leave: '+tocon)
#	sleep(len(confbase)/2)

#error handler
debugmode = 0
def errorHandler(text):
        pprint(u'\n*** Error ***')
        pprint(text)
        pprint(u'more info at http://isida.googlecode.com\n')
        exit (0)

dm = 1
prefix = u'_'
msg_limit = 1000
botName = 'Isida-Bot'
botVersion = 'v1.7'
capsVersion = botVersion[1:]
banbase = []
iq_answer = []
timeout = 300

gt=gmtime()
lt=untime(localtime())

if lt[0:3] == gt[0:3]:
        timeofset = int(lt[3])-int(gt[3])
elif lt[0:3] > gt[0:3]:
        timeofset = int(lt[3])-int(gt[3]) + 24
else:
        timeofset = int(gt[3])-int(lt[3]) + 24

if os.path.isfile(ver_file):
	bvers = str(readfile(ver_file))
	if len(bvers[:-1]) > 1:
        	botVersion += '.' + bvers[:-1]

# --- load config.txt

if os.path.isfile(configname):
        execfile(configname)
else:
        errorHandler(configname+u' is missed.')

capsNode = 'http://isida.googlecode.com'

# --- check parameters

baseParameters = [nickname ,name, domain, password, newBotJid, mainRes, SuperAdmin, defaultConf, CommStatus, StatusMessage, Priority]

baseErrors = [u'nickname', u'name', u'domain', u'password', u'newBotJid', u'mainRes', u'SuperAdmin', u'defaultConf', u'CommStatus', u'StatusMessage', u'Priority']

megabase = []
megabase2 = []

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
execfile('plugins/main.py')
plname = u'plugins/list.txt'

if os.path.isfile(plname):
        plugins = eval(readfile(plname))
        for pl in plugins:
                pprint('Append plugin: '+pl)
                execfile('plugins/'+pl)
                for commmm in execute:
                        comms.append(commmm)
else:
	plugins = []
	writefile(plname,str(plugins))

if os.path.isfile(alfile):
	aliases = eval(readfile(alfile))
else:
	aliases = []

def send_msg(mtype, mjid, mnick, mmessage):
	if len(mmessage):
	        no_send = 1
	        log_limit = 50
        	if len(mmessage) <= log_limit:
        	        log_record = mmessage
        	else:
        	        log_record = mmessage[:log_limit] + ' [+' + str(len(mmessage)) +']'

#		pprint('['+mtype+'] '+log_record+' ['+mjid+'/'+mnick+']')
        	if len(mmessage) > msg_limit:
        	        cnt = 0
        	        maxcnt = len(mmessage)/msg_limit + 1
        	        mmsg = mmessage
        	        while len(mmsg) > msg_limit:
        	                tmsg = '['+str(cnt+1)+'/'+str(maxcnt)+'] '+mmsg[:msg_limit]+'[...]'
                        
        	                cnt += 1
        	                cl.send(xmpp.Message(mjid+'/'+mnick, tmsg, 'chat'))
        	                mmsg = mmsg[msg_limit:]
        	                sleep(1)
        	                
        	        tmsg = '['+str(cnt+1)+'/'+str(maxcnt)+'] '+mmsg
        	        cl.send(xmpp.Message(mjid+'/'+mnick, tmsg, 'chat'))
        	        if mtype == 'chat':
        	                no_send = 0
        	        else:
        	                mmessage = mmessage[:msg_limit] + '[...]'
	
        	if no_send:
        	        if mtype == 'groupchat' and mnick != '':
        	                mmessage = mnick+': '+mmessage
        	        else:
        	                mjid += '/' + mnick
	
			while mmessage[-1:] == '\n' or mmessage[-1:] == '\t' or mmessage[-1:] == '\r' or mmessage[-1:] == ' ':
				mmessage = mmessage[:-1]
	
			if len(mmessage):
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
	zz = join(conf)
	if zz != None:
		pprint(' *** Error *** '+zz)
	return zz

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
def onoff(msg):
        if msg:
                return 'ON'
        else:
                return 'OFF'

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
	global iq_answer
	j = Presence(conference, show=CommStatus, status=StatusMessage, priority=Priority)
	j.setTag('x', namespace=NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
	j.getTag('x').setTagData('password', psw)
	j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})

	cl.send(j)
	id=j.getID()
	Error = None
	for aa in range(0,5):
		for bb in iq_answer:
			if bb[0]==id:
				Error = bb[1]
				break
		if Error != None:
			break
		sleep(0.1)
	return Error

def leave(conference, sm):
    j = Presence(conference, 'unavailable', status=sm)
    j.setTag('x', namespace=NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
    j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
    cl.send(j)

def timeZero(val):
    rval = []
    for iv in range(0,len(val)):
        if val[iv]<10:
            rval.append('0'+str(val[iv]))
        else:
            rval.append(str(val[iv]))
    return rval

def iqCB(sess,iq):
	global timeofset, banbase, iq_answer
        nick = unicode(iq.getFrom())
        id = iq.getID()
        query = iq.getTag('query')

	if iq.getType()=='error':
		iq_answer.append((id,iq.getTag('error').getTagData(tag='text')))

	if iq.getType()=='result':
		cparse = unicode(iq)
		nspace = query.getNamespace()
                if nspace == NS_MUC_ADMIN:
#                        ccount = cparse.count('<item affiliation=\"outcast\"')
                        cparse = cparse.split('<item')
			banbase = []
                        for banm in cparse[1:]:
				st_index = banm.find('jid=\"')+5
				cjid=banm[st_index:banm.find('\"',st_index)]
				if banm.count('<reason />') or banm.count('<reason/>'):
					creason = u'No reason'
				else:
					creason=banm[banm.find('<reason>')+8:banm.find('</reason>')]
				banbase.append((cjid, creason))
			banbase.append((u'TheEnd', u'None'))

		if nspace == NS_VERSION:
				iq_answer.append((id, iq.getTag('query').getTagData(tag='name'), iq.getTag('query').getTagData(tag='version'),iq.getTag('query').getTagData(tag='os')))

		if nspace == NS_TIME:
				iq_answer.append((id, iq.getTag('query').getTagData(tag='display'),iq.getTag('query').getTagData(tag='utc'),iq.getTag('query').getTagData(tag='tz')))

	if iq.getType()=='get':
		if iq.getTag(name='query', namespace=xmpp.NS_VERSION):
			pprint(u'*** iq:version from '+unicode(nick))
                        i=xmpp.Iq(to=nick, typ='result')
                        i.setAttr(key='id', val=id)
                        i.setQueryNS(namespace=xmpp.NS_VERSION)
                        i.getTag('query').setTagData(tag='name', val=botName)
                        i.getTag('query').setTagData(tag='version', val=botVersion)
                        i.getTag('query').setTagData(tag='os', val=botOs)
                        cl.send(i)
			raise xmpp.NodeProcessed

                if iq.getTag(name='query', namespace=xmpp.NS_TIME):
			pprint(u'*** iq:time from '+unicode(nick))
                        gt=timeZero(gmtime())
                        t_utc=gt[0]+gt[1]+gt[2]+'T'+gt[3]+':'+gt[4]+':'+gt[5]
                        
                        lt=untime(localtime())
                        ltt=timeZero(lt)
                        wday = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
                        wlight = ['Winter','Summer']
                        wmonth = ['Jan','Fed','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                        
                        t_display = ltt[3]+':'+ltt[4]+':'+ltt[5]+', '+ltt[2]+'.'+wmonth[lt[1]-1]+'\''+ltt[0]+', '+wday[lt[6]]+', '

                        if timeofset < 0:
                                t_tz = 'GMT'+str(timeofset)
                        else:
                                t_tz = 'GMT+'+str(timeofset)
			t_display += t_tz + ', ' +wlight[lt[8]]+' time'
                        
                        i=xmpp.Iq(to=nick, typ='result')
                        i.setAttr(key='id', val=id)
                        i.setQueryNS(namespace=xmpp.NS_TIME)
                        i.getTag('query').setTagData(tag='utc', val=t_utc)
                        i.getTag('query').setTagData(tag='tz', val=t_tz)
                        i.getTag('query').setTagData(tag='display', val=t_display)
                        cl.send(i)
			raise xmpp.NodeProcessed

def com_parser(access_mode, nowname, type, room, nick, text, jid):
	no_comm = 1
	for parse in comms:
		if access_mode >= parse[0] and nick != nowname:
        	        if text.lower() == parse[1].lower() or text[:len(parse[1])+1].lower() == parse[1].lower()+' ':
				pprint(jid+' '+room+'/'+nick+' ['+str(access_mode)+'] '+text)
				no_comm = 0
                                if not parse[3]:
                                        thread.start_new_thread(thread_log,(parse[2], type, room, nick, par))
       	                        elif parse[3] == 1:
       	                                thread.start_new_thread(thread_log,(parse[2], type, room, nick))
       	                        elif parse[3] == 2:
                                        thread.start_new_thread(thread_log,(parse[2], type, room, nick, text[len(parse[1])+1:]))
				break
	return no_comm

def messageCB(sess,mess):
        global otakeRes, mainRes, psw, lfrom, lto, owners, ownerbase, confbase, confs, lastserver, lastnick, comms
        global ignorebase, ignores
        room=unicode(mess.getFrom().getStripped())
        nick=unicode(mess.getFrom().getResource())
        text=unicode(mess.getBody())
        type=unicode(mess.getType())
        towh=unicode(mess.getTo().getStripped())
	stamp=unicode(mess.getTimestamp())

	lprefix = get_local_prefix(room)

#        print '---\n',parser(room), parser(nick), parser(text), parser(type), parser(towh), parser(stamp)

        rn = room+"/"+nick

        text=unicode(text)

# 0 - конфа # 1 - ник # 2 - роль # 3 - аффиляция # 4 - jid

        ft = text

        ta = get_access(room,nick)

        access_mode = ta[0]
        jid =ta[1]

	tmppos = arr_semi_find(confbase, room)
	if tmppos == -1:
		nowname = nickname
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '':
			nowname = nickname

	if jid == 'None' and ownerbase.count(getRoom(room)):
		access_mode = 2

        if type == 'groupchat' and nick != '' and jid != 'None':
                talk_count(room,jid,nick,text)
	no_comm = 1
        if (text != 'None') and (len(text)>=1) and access_mode >= 0:
		no_comm = 1
		is_par = 0
		if text[:len(nowname)] == nowname:
			text = text[len(nowname)+2:]
			is_par = 1
		btext = text
		if text[:len(lprefix)] == lprefix:
			text = text[len(lprefix):]
			is_par = 1
		if type == 'chat':
			is_par = 1
		if is_par:
			no_comm = com_parser(access_mode, nowname, type, room, nick, text, jid)

		if no_comm:
			for parse in aliases:
				if btext.lower() == parse[1].lower() or btext[:len(parse[1])+1].lower() == parse[1].lower()+' ':
					pprint(jid+' '+room+'/'+nick+' ['+str(access_mode)+'] '+text)
					ppr = parse[2].replace('%*',text[len(parse[1])+1:])
					no_comm = com_parser(access_mode, nowname, type, room, nick, ppr, jid)
					break

	is_flood = 0
	if room != selfjid:
		if os.path.isfile(fld):
			floods = eval(readfile(fld))
		else:
			floods = [(getRoom(room),0)]
			writefile(fld,str(floods))
		for sm in floods:
			if sm[0] == getRoom(room) and sm[1]:
				is_flood = 1
				break

	if no_comm and access_mode >= 0 and (ft[:len(nowname)+2] == nowname+': ' or ft[:len(nowname)+2] == nowname+', ' or type == 'chat') and is_flood:
		if len(text)>100:
			text = u'Слишком многа букаф!'
		else:
			text = getAnswer(text,type)
		send_msg(type, room, nick, text)

# исправить этот костыль!!!
def thread_log(proc, *params):
        try:
                if len(params) == 3:
                        proc(params[0], params[1], params[2])
                else:
                        proc(params[0], params[1], params[2], params[3])
        except:
                logging.exception(' ['+timeadd(untime(localtime()))+'] ')

def getAnswer(tx,type):
	mdb = sqlite3.connect(mainbase)
	answers = mdb.cursor()
	la = len(answers.execute('select * from answer').fetchall())
	mrand = str(randint(1,la))
	answers.execute('select * from answer where ind=?', (mrand,))

	for aa in answers:
		anscom = aa[1]

        if type == 'groupchat':
		tx = to_censore(tx)
		answers.execute('insert into answer values (?,?)', (la+1,tx))
	mdb.commit()

        anscom = to_censore(anscom)
	return anscom

def to_censore(text):
        for c in censor:
                if text.count(c):
                        text = text.replace(c,'[censored]')
        return text

def compare(aa,bb):
	kpd = 0
	aa = aa.split(' ')
	bb = bb.split(' ')
	for a in aa:
		for b in bb:
			if len(a)>len(b):
				ll = len(b)
			else:
				ll = len(a)
			for c in range(0,ll):
				if operator.xor(ord(a[c]),ord(b[c])) <= 3:
					kpd += 1
	return kpd

def presenceCB(sess,mess):
	global megabase, megabase2, ownerbase, iq_answer, confs, confbase
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
	id = mess.getID()
        to=unicode(mess.getTo())

	if type=='error':
		iq_answer.append((id,mess.getTag('error').getTagData(tag='text')))

	if jid == 'None':		
	        ta = get_access(room,nick)
	        jid =ta[1]

	tmppos = arr_semi_find(confbase, room)
	if tmppos == -1:
		nowname = nickname
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '':
			nowname = nickname

	if room != selfjid and nick == nowname:
		if os.path.isfile(sml):
			smiles = eval(readfile(sml))
		else:
			smiles = [(getRoom(room),0)]
			writefile(sml,str(smiles))
		for sm in smiles:
			if sm[0] == getRoom(room) and sm[1]:
				msg = u''
				if role == 'participant' and affiliation == 'none':
					msg = u' :-|'
				if role == 'participant' and affiliation == 'member':
					msg = u' :-)'
				if role == 'moderator' and affiliation == 'member':
					msg = u' :-"'
				if role == 'moderator' and affiliation == 'admin':
					msg = u' :-D'
				if role == 'moderator' and affiliation == 'owner':
					msg = u' 8-D'
				nick = ''
				type = 'groupchat'
				if msg != u'':
					send_msg(type, room, nick, msg)
				break


#	print room, nick, text, role, affiliation, jid, priority, show, reason, type, status, actor
	
	if ownerbase.count(getRoom(room)) and type != 'unavailable':
		j = Presence(room, show=CommStatus, status=StatusMessage, priority=Priority)
		j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
		cl.send(j)

	if type=='unavailable':
		for mmb in megabase:
			if mmb[0]==room and mmb[1]==nick:
				megabase.remove(mmb)
		if to == selfjid and (status=='307' or status=='301') and confbase.count(room+'/'+nick):
			if os.path.isfile(confs):
				confbase = eval(readfile(confs))
				confbase = arr_del_semi_find(confbase,getRoom(room))
        	                writefile(confs,str(confbase))
	else:
		not_found = 1
		for mmb in megabase:
			if mmb[0]==room and mmb[1]==nick:
				megabase.remove(mmb)
				megabase.append([room, nick, role, affiliation, jid])
				not_found = 0
		if not_found:
			megabase.append([room, nick, role, affiliation, jid])

	if not megabase2.count([room, nick, role, affiliation, jid]):
		megabase2.append([room, nick, role, affiliation, jid])

	if jid != 'None':
		mdb = sqlite3.connect(mainbase)
		cu = mdb.cursor()
		aa1 = jid[:jid.index('@')]
		aa2 = jid[jid.index('@')+1:jid.index('/')]
		aa3 = jid[jid.index('/')+1:]
		if not cu.execute('select * from jid where login=? and server=? and resourse=?',(aa1,aa2,aa3)).fetchall():
			cu.execute('insert into jid values (?,?,?)', (aa1,aa2,aa3))
			mdb.commit()

	if jid != 'None':
		jid = getRoom(jid.lower())
		mdb = sqlite3.connect(mainbase)
		cu = mdb.cursor()
		abc = cu.execute('select * from age where room=? and jid=?',(room, jid)).fetchall()
		tt = int(time.time())
		cu.execute('delete from age where room=? and jid=?',(room, jid))
		for ab in abc:
			if type=='unavailable':
#				print status
				exit_type = ''
				exit_message = ''
				if status=='307': #Kick
					exit_type = u'Выгнали'
					exit_message = reason
				elif status=='301': #Ban
					exit_type = u'Забанили'
					exit_message = reason
				else: #Leave
					exit_type = u'Вышел'
					exit_message = show
				if exit_message == 'None':
					exit_message = ''
#				print exit_type, exit_message
				cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (room, nick,getRoom(jid.lower()),tt,ab[4]+(tt-ab[3]),1,exit_type,exit_message))
			else:
				if ab[5]:
					cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (room,nick,getRoom(jid.lower()),tt,ab[4],0,ab[6],ab[7]))
				else:
					cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (room,nick,getRoom(jid.lower()),ab[3],ab[4],0,ab[6],ab[7]))
		if not len(abc):
			cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (room,nick,getRoom(jid.lower()),tt,0,0,'',''))
		mdb.commit()

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

def schedule():
	lt=untime(localtime())
	l_hi = (lt[0]*400+lt[1]*40+lt[2]) * 86400
	l_lo = lt[3]*3600+lt[4]*60+lt[5]

	try:
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
			ll_hi = (lttime[0]*400+lttime[1]*40+lttime[2]) * 86400
			ll_lo = lttime[3]*3600+lttime[4]*60+lttime[5]
	
			if ll_hi + ll_lo + ofset <= l_lo + l_hi:
				pprint(u'check rss: '+fd[0]+u' in '+fd[4])
				type = 'groupchat'
				jid = fd[4]
				nick = 'RSS'
				text = 'new '+fd[0]+' 10 '+fd[2]+' silent'
				thread.start_new_thread(thread_log,(rss, type, jid, nick, text))
#				rss(type, jid, nick, text)
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
	
				lt=untime(localtime())
				text = text.split(' ')
				link = text[1]
				if link[:7] != 'http://':
        			        link = 'http://'+link
				feedbase.append([link, text[2], text[3], lt[:6], jid])
				writefile(feeds,str(feedbase))
				sleep(0.1)
	except:
		sleep(0.1)

def talk_count(room,jid,nick,text):

        jid = getRoom(jid)

	mdb = sqlite3.connect(mainbase)
	cu = mdb.cursor()
	tlen = len(cu.execute('select * from talkers where room=? and jid=?',(room,jid)).fetchall())
	cu.execute('select * from talkers where room=? and jid=?',(room,jid))

        wtext = text.split(' ')
        wtext = len(wtext)
        beadd = 1

	if tlen:
		for aa in cu:
			ab=aa
		cu.execute('delete from talkers where room=? and jid=?',(room,jid))
		cu.execute('insert into talkers values (?,?,?,?,?)', (ab[0],ab[1],nick,ab[3]+wtext,ab[4]+1))
	else:
		cu.execute('insert into talkers values (?,?,?,?,?)', (room, jid, nick, wtext, 1))
	mdb.commit()

# ---------- HERE WE GO!!! -----------

if os.path.isfile('settings/starttime'):
	try:
		starttime = eval(readfile('settings/starttime'))
	except:
		starttime = readfile('settings/starttime')
		starttime = untime(starttime)
else:
	starttime = untime(localtime())

sesstime = int(time.time())

mtb = os.path.isfile(mainbase)

mdb = sqlite3.connect(mainbase)
cu = mdb.cursor()
if not mtb:
	cu.execute('''create table age (room text, nick text, jid text, time integer, age integer, status integer, type text, message text)''')
	cu.execute('''create table answer (ind integer, body text)''')
	cu.execute('''create table jid (login text, server text, resourse text)''')
	cu.execute('''create table talkers (room text, jid text, nick text, words integer, frases integer)''')
	cu.execute('''create table wtf (ind integer, room text, jid text, nick text, wtfword text, wtftext text, time text)''')
	cu.execute('insert into answer values (?,?)', (1,u';-)'))
	cu.execute('insert into answer values (?,?)', (2,u'Привет'))
	mdb.commit()

if os.path.isfile(owners):
	ownerbase = eval(readfile(owners))
else:
	ownerbase = [god]
	writefile(owners,str(ownerbase))

if os.path.isfile(ignores):
	ignorebase = eval(readfile(ignores))
else:
	ignorebase = []
	writefile(ignores,str(ignorebase))

close_age_null()

if os.path.isfile(confs):
	confbase = eval(readfile(confs))
else:
	confbase = [defaultConf+u'/'+nickname]
	writefile(confs,str(confbase))

if os.path.isfile(cens):
	censor = readfile(cens).decode('UTF')
	censor = censor.split('\n')
	for c in censor:
                if c.count('#') or not len(c):
                        censor.remove(c)
else:
	censor = []

pprint(u'****************************')
pprint(u'*** Bot Name: '+botName)
pprint(u'*** Version '+botVersion)
pprint(u'*** OS '+botOs)
pprint(u'******************************')
pprint(u'*** (c) 2oo9 Disabler Production Lab.')

node = unicode(name)
lastnick = nickname

jid = JID(node=node, domain=domain, resource=mainRes)
selfjid = jid

pprint(u'bot jid: '+unicode(jid))

psw = u''

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

pprint(u'Wait conference')
for tocon in confbase:
	baseArg = unicode(tocon)
	if not tocon.count('/'):
		baseArg += u'/'+unicode(nickname)
	conf = JID(baseArg)
	pprint(tocon)
	sleep(0.2)
	zz = join(conf)
	if zz != None:
		pprint(' *** Error *** '+zz)

cl.RegisterHandler('message',messageCB)
cl.RegisterHandler('iq',iqCB)
cl.RegisterHandler('presence',presenceCB)
cl.sendInitPresence()

lastserver = getServer(confbase[0])

pprint(u'Joined')

game_over = 0

while 1:
	try:
		while not game_over:
        		cl.Process(1)
			schedule()
		close_age()
		break

	except KeyboardInterrupt:
		close_age()
		StatusMessage = 'Shut down by CTRL+C'
		pprint(StatusMessage)
		send_presence_all(StatusMessage)
        	writefile(tmpf,str('exit'))
		sleep(2)
		sys.exit(0)

	except Exception, SM:
#		close_age()
		pprint('*** Error *** '+str(SM)+' ***')
                logging.exception(' ['+timeadd(untime(localtime()))+'] ')
                if debugmode:
                        writefile(tmpf,str('exit'))
        		raise


