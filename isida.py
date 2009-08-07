#!/usr/bin/python
# -*- coding: utf -*-
from xmpp import *
from sys import argv
from random import *
from sys import maxint
from time import *
from pdb import *
from subprocess import Popen, PIPE, STDOUT
import os, xmpp, time, sys, time, pdb, urllib, urllib2, re, logging
import thread, operator, sqlite3, simplejson, chardet, socket, popen2, atexit

LOG_FILENAME = u'log/error.txt'		# логи

set_folder = u'settings/'		# папка настроек
back_folder = u'backup/'		# папка хронения резервных копий

preffile = set_folder+u'prefix'		# префиксы
ver_file = set_folder+u'version'	# версия бота
configname = set_folder+u'config.py'	# конфиг бота
alfile = set_folder+u'aliases'		# сокращения
fld = set_folder+u'flood'		# автоответчик
sml = set_folder+u'smile'		# смайлы на роли
cns = set_folder+u'censors'		# состояние цензора
owners = set_folder+u'owner'		# база владельцев
ignores = set_folder+u'ignore'		# черный список
confs = set_folder+u'conf'		# список активных конф
tmpf = set_folder+u'tmp'		# флаг завершения бота
feeds = set_folder+u'feed'		# список rss каналов
lafeeds = set_folder+u'lastfeeds'	# последние новости по каждому каналу
cens = set_folder+u'censor.txt'		# список "запрещенных" слов для болтуна
conoff = set_folder+u'commonoff'	# список "запрещенных" команд для бота

saytobase = set_folder+u'sayto.db'	# база команды "передать"
agestatbase = set_folder+u'agestat.db'	# статистика возрастов
jid_base = set_folder+u'jidbase.db'	# статистика jid'ов
talkersbase = set_folder+u'talkers.db'	# статистика болтунов
wtfbase = set_folder+u'wtfbase.db'	# определения
answersbase = set_folder+u'answers.db'	# ответы бота

logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

global execute, prefix, comms, prev_time

prev_time = int(time.time())

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

def getFile(filename,default):
	if os.path.isfile(filename):
		while 1:
			try:
				filebody = eval(readfile(filename))
				break
			except:
				sleep(0.5)
	else:
		filebody = default
		writefile(filename,str(filebody))
	return filebody

def get_subtag(body,tag):
	beg = body.find('\"',body.find(tag))+1
	return body[beg:body.find('\"',beg)]

def get_tag(body,tag):
	return body[body.find('>',body.find('<'+tag))+1:body.find('</'+tag+'>')]

def get_tag_full(body,tag):
	return body[body.find('<'+tag):body.find(tag+'>',body.find('<'+tag)+2)+len(tag)+1]

def parser(text):
	logt=tuple(localtime())
	logfile = 'log/'+tZ(logt[0])+tZ(logt[1])+tZ(logt[2])

	log = getFile(logfile,[])
	log.append(text)
	writefile(logfile,str(log))

	text = unicode(text)
	ttext = u''
	i = 0
	while i<len(text):
		if (text[i]<='~'): ttext+=text[i]
		else: ttext+='?'
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

def onlytimeadd(lt):
	st = tZ(lt[3])+u':'+tZ(lt[4])+u':'+tZ(lt[5])
	return st

def pprint(text):
	global dm
	text = text
	zz = parser('['+timeadd(tuple(localtime()))+'] '+text)
	if not dm: print zz

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
botVersion = 'v1.8'
capsVersion = botVersion[1:]
banbase = []
iq_answer = []
timeout = 300

gt=gmtime()
lt=tuple(localtime())

if lt[0:3] == gt[0:3]: timeofset = int(lt[3])-int(gt[3])
elif lt[0:3] > gt[0:3]: timeofset = int(lt[3])-int(gt[3]) + 24
else: timeofset = int(gt[3])-int(lt[3]) + 24

if os.path.isfile(ver_file):
	bvers = str(readfile(ver_file))
	if len(bvers[:-1]) > 1: botVersion += '.' + bvers[:-1]

# --- load config.txt

if os.path.isfile(configname): execfile(configname)
else: errorHandler(configname+u' is missed.')

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
gtimer = []
gpresence = []
gmessage = []

if os.path.isfile(plname):
	plugins = eval(readfile(plname))
	for pl in plugins:
		presence_control = []
		message_control = []
		iq_control = []
		timer = []
		pprint('Append plugin: '+pl)
		execfile('plugins/'+pl)
		for cm in execute:
			comms.append((cm[0],cm[1],cm[2],cm[3],u'Плагин '+pl[:-3]+'. '+cm[4]))
		for tmr in timer:
			gtimer.append(tmr)
		for tmp in presence_control:
			gpresence.append(tmp)
		for tmp in message_control:
			gmessage.append(tmp)
else:
	plugins = []
	writefile(plname,str(plugins))


aliases = getFile(alfile,[])

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
			return get_registry_value("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",key)
		osInfo = get("ProductName")
		buildInfo = get("CurrentBuildNumber")
		try:
			spInfo = get("CSDVersion")
			japytOs = osInfo+' '+spInfo+' (Build: '+buildInfo+') / Python v'+japytPyVer
		except:
			japytOs = osInfo+' (Build: '+buildInfo+') / Python v'+japytPyVer
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
	global timeofset, banbase, iq_answer, raw_iq
	nick = unicode(iq.getFrom())
	id = iq.getID()
	query = iq.getTag('query')

	if iq.getType()=='error':
		try:
			iq_answer.append((id,iq.getTag('error').getTagData(tag='text')))
		except:
			iq_answer.append((u'Неизвесная ошибка!'))

	if iq.getType()=='result':
		cparse = unicode(iq)
		raw_iq = [id,cparse]
		nspace = query.getNamespace()
		if nspace == NS_MUC_ADMIN:
#			ccount = cparse.count('<item affiliation=\"outcast\"')
			cparse = cparse.split('<item')
			for banm in cparse[1:]:
				st_index = banm.find('jid=\"')+5
				cjid=banm[st_index:banm.find('\"',st_index)]
				if banm.count('<reason />') or banm.count('<reason/>'):
					creason = u'No reason'
				else:
					creason=banm[banm.find('<reason>')+8:banm.find('</reason>')]
				banbase.append((cjid, creason, str(id)))
			banbase.append((u'TheEnd', u'None',str(id)))
		if nspace == NS_MUC_OWNER:
			banbase.append((u'TheEnd', u'None',str(id)))
		if nspace == NS_VERSION:
				iq_answer.append((id, iq.getTag('query').getTagData(tag='name'), iq.getTag('query').getTagData(tag='version'),iq.getTag('query').getTagData(tag='os')))

		if nspace == NS_TIME:
				iq_answer.append((id, iq.getTag('query').getTagData(tag='display'),iq.getTag('query').getTagData(tag='utc'),iq.getTag('query').getTagData(tag='tz')))
		if nspace == NS_DISCO_ITEMS:
				iq_answer.append((id, unicode(iq)))
		if nspace == NS_LAST:
				iq_answer.append((id, unicode(iq)))

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
			
			lt=tuple(localtime())
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
	cof = getFile(conoff,[])
	for parse in comms:
		if access_mode >= parse[0] and nick != nowname:
			not_offed = 1
			if access_mode != 2:
				for co in cof:
					if co[0]==room and co[1]==text.lower()[:len(co[1])]:
						not_offed = 0
						break
			if not_offed and (text.lower() == parse[1].lower() or text[:len(parse[1])+1].lower() == parse[1].lower()+' '):
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

	back_text = text

#	print '---\n', 'room:',parser(room),'\nnick:',parser(nick),'\ntext:',parser(text),'\ntype:', parser(type),'\ntowh:',parser(towh),'\nstamp:', parser(stamp)

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

	if nick != '' and nick != 'None' and nick != nowname and len(text)>1 and text != 'None' and text != to_censore(text) and access_mode >= 0:
		gl_censor = getFile(cns,[(getRoom(room),0)])
		if (getRoom(room),1) in gl_censor:
			send_msg(type,room,nick,u'Фильтруем базар!')


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
				if (btext.lower() == parse[1].lower() or btext[:len(parse[1])+1].lower() == parse[1].lower()+' ') and room == parse[0]:
					
					pprint(jid+' '+room+'/'+nick+' ['+str(access_mode)+'] '+text)
					ppr = parse[2].replace('%*',btext[len(parse[1])+1:])
					no_comm = com_parser(access_mode, nowname, type, room, nick, ppr, jid)
					break

	if room != selfjid:
		floods = getFile(fld,[(getRoom(room),0)])
		is_flood = (getRoom(room),1) in floods
	else:
		is_flood = 0

	if no_comm and access_mode >= 0 and (ft[:len(nowname)+2] == nowname+': ' or ft[:len(nowname)+2] == nowname+', ' or type == 'chat') and is_flood:
		if len(text)>100:
			text = u'Слишком многа букаф!'
			send_msg(type, room, nick, text)
		else:
			text = getAnswer(text,type)
			thread.start_new_thread(send_msg_human,(type, room, nick, text))


	for tmp in gmessage:
		try:
			subj=unicode(mess.getSubject())
			if subj != 'None' and back_text == 'None':
				thread.start_new_thread(message_thread,(tmp,room,jid,'',type,u'*** '+nick+u' обновил(а) тему: '+subj))
			else:
				thread.start_new_thread(message_thread,(tmp,room,jid,nick,type,back_text))
		except:
			sleep(0.1)
					
def message_thread(*param):
	param[0](param[1],param[2],param[3],param[4],param[5])
	sys.exit(0)

def send_msg_human(type, room, nick, text):
	sleep(len(text)/4)
	send_msg(type, room, nick, text)
	sys.exit(0)	

# исправить этот костыль!!!
def thread_log(proc, *params):
	try:
		if len(params) == 3:
			proc(params[0], params[1], params[2])
		else:
			proc(params[0], params[1], params[2], params[3])
	except:
		logging.exception(' ['+timeadd(tuple(localtime()))+'] ')
	sys.exit(0)

def getAnswer(tx,type):
	mdb = sqlite3.connect(answersbase)
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
#		print c
		matcher = re.compile(r'.*'+c.lower()+r'.*')
		if matcher.match(r' '+text.lower()+r' '):
			text = '*censored*'
			break
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
		smiles = getFile(sml,[(getRoom(room),0)])
		if (getRoom(room),1) in smiles:
			msg = u''
			if role == 'participant' and affiliation == 'none':
				msg = u' :-|'
			elif role == 'participant' and affiliation == 'member':
				msg = u' :-)'
			elif role == 'moderator' and affiliation == 'member':
				msg = u' :-"'
			elif role == 'moderator' and affiliation == 'admin':
				msg = u' :-D'
			elif role == 'moderator' and affiliation == 'owner':
				msg = u' 8-D'
			if msg != u'':
				send_msg('groupchat', room, '', msg)

#	print room, nick, text, role, affiliation, jid, priority, show, reason, type, status, actor
	
	if ownerbase.count(getRoom(room)) and type != 'unavailable':
		j = Presence(room, show=CommStatus, status=StatusMessage, priority=Priority)
		j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
		cl.send(j)

	not_found = 0
	if type=='unavailable' and nick != '':
		for mmb in megabase:
			if mmb[0]==room and mmb[1]==nick:
				megabase.remove(mmb)
		if to == selfjid and (status=='307' or status=='301') and confbase.count(room+'/'+nick):
			if os.path.isfile(confs):
				confbase = eval(readfile(confs))
				confbase = arr_del_semi_find(confbase,getRoom(room))
				writefile(confs,str(confbase))
	elif nick != '':

		sdb = sqlite3.connect(saytobase)
		cu = sdb.cursor()
		cm = cu.execute('select * from st where room=? and (jid=? or jid=?)',(room, getRoom(jid), nick)).fetchall()
		if len(cm):
			cu.execute('delete from st where room=? and (jid=? or jid=?)',(room, getRoom(jid), nick))
			for cc in cm:
				if cc[0].count('\n'):
					zz = cc[0].split('\n')
					send_msg('chat', room, nick, zz[0]+' ('+un_unix(time.time()-int(zz[1]))+u' назад) просил передать: '+cc[3])
				else:
					send_msg('chat', room, nick, cc[0]+u' просил передать: '+cc[3])
			sdb.commit()
		for mmb in megabase:
			if mmb[0]==room and mmb[1]==nick:
				megabase.remove(mmb)
				megabase.append([room, nick, role, affiliation, jid])
				if role != mmb[2] or affiliation != mmb[3]: not_found = 1
				else: not_found = 2
		if not not_found:
			megabase.append([room, nick, role, affiliation, jid])

	if not megabase2.count([room, nick, role, affiliation, jid]):
		megabase2.append([room, nick, role, affiliation, jid])

	if jid != 'None':
		mdb = sqlite3.connect(jid_base)
		cu = mdb.cursor()
		aa1 = jid[:jid.index('@')]
		aa2 = jid[jid.index('@')+1:jid.index('/')]
		aa3 = jid[jid.index('/')+1:]
		if not cu.execute('select * from jid where login=? and server=? and resourse=?',(aa1,aa2,aa3)).fetchall():
			cu.execute('insert into jid values (?,?,?)', (aa1,aa2,aa3))
			mdb.commit()

	if jid == 'None':
		jid = '<temporary>'+nick
	else:
		jid = getRoom(jid.lower())


	mdb = sqlite3.connect(agestatbase)
	cu = mdb.cursor()
	abc = cu.execute('select * from age where room=? and jid=?',(room, jid)).fetchall()
	tt = int(time.time())
	cu.execute('delete from age where room=? and jid=?',(room, jid))

	ttext = role + '\n' + affiliation + '\n' + priority + '\n' + show  + '\n' + text

	exit_type = ''
	exit_message = ''
	for ab in abc:
		if type=='unavailable':
			if status=='307': #Kick
				exit_type = u'Выгнали'
				exit_message = reason
			elif status=='301': #Ban
				exit_type = u'Забанили'
				exit_message = reason
			else: #Leave
				exit_type = u'Вышел'
				exit_message = text
			if exit_message == 'None':
				exit_message = ''
#				print exit_type, exit_message
			cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (room, nick,getRoom(jid.lower()),tt,ab[4]+(tt-ab[3]),1,exit_type,exit_message))
		else:
			if ab[5]:
				cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (room,nick,getRoom(jid.lower()),tt,ab[4],0,ab[6],ttext))
			else:
				cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (room,nick,getRoom(jid.lower()),ab[3],ab[4],0,ab[6],ttext))
	if not len(abc):
		cu.execute('insert into age values (?,?,?,?,?,?,?,?)', (room,nick,getRoom(jid.lower()),tt,0,0,'',ttext))
	mdb.commit()

	for tmp in gpresence:
		try: thread.start_new_thread(presence_thread,(tmp,room,jid,nick,type,(text, role, affiliation, exit_type, exit_message, show, priority, not_found)))
		except: sleep(0.1)

def presence_thread(*param):
	param[0](param[1],param[2],param[3],param[4],param[5])
	sys.exit(0)
	
def onoff(msg):
	if msg: return 'ON'
	else: return 'OFF'

def getName(jid):
	jid = unicode(jid)
	return jid[:jid.find('@')]

def getServer(jid):
	jid = unicode(jid)
	if not jid.count('/'): jid += '/'
	return jid[jid.find('@')+1:jid.find('/')]

def getResourse(jid):
	jid = unicode(jid)
	return jid[jid.find('/')+1:]

def getRoom(jid):
	jid = unicode(jid)
	return getName(jid)+'@'+getServer(jid)

def schedule():
	global prev_time
	tmp_time = int(time.time())
	if tmp_time > prev_time:
		prev_time = tmp_time
		now_schedule()

def timer_thread(*param):
	param[0]()
	sys.exit(0)
		
def now_schedule():
	for tmr in gtimer:
		try: thread.start_new_thread(timer_thread,(tmr,))
		except: sleep(0.01)

	lt=tuple(localtime())
	if lt[5]/20 == lt[5]/20.0:
		l_hl = (lt[0]*400+lt[1]*40+lt[2]) * 86400 + lt[3]*3600+lt[4]*60+lt[5]
		try:
			feedbase = getFile(feeds,[])
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
				ll_hl = (lttime[0]*400+lttime[1]*40+lttime[2]) * 86400 + lttime[3]*3600+lttime[4]*60+lttime[5]
		
				if ll_hl + ofset <= l_hl:
					pprint(u'check rss: '+fd[0]+u' in '+fd[4])
					thread.start_new_thread(thread_log,(rss, 'groupchat', fd[4], 'RSS', 'new '+fd[0]+' 10 '+fd[2]+' silent'))
					feedbase.remove(fd)
					feedbase.append([fd[0], fd[1], fd[2], lt[:6], fd[4]])
			writefile(feeds,str(feedbase))
			sleep(0.01)
		except:
			sleep(0.01)
	else:
		sleep(0.01)

def talk_count(room,jid,nick,text):

	jid = getRoom(jid)

	mdb = sqlite3.connect(talkersbase)
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
		starttime = tuple(starttime)
else:
	starttime = tuple(localtime())

sesstime = int(time.time())

ownerbase = getFile(owners,[god])
ignorebase = getFile(ignores,[])
close_age_null()
confbase = getFile(confs,[defaultConf+u'/'+nickname])

if os.path.isfile(cens):
	censor = readfile(cens).decode('UTF')
	censor = censor.split('\n')
	cn = []
	for c in censor:
		if (not c.count('#')) and len(c):
			cn.append(c)
	censor = cn
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
raw_iq = []

try:
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
except:
	reboot_time = 60
	pprint(u'Auth error or no connection. Restart in '+str(reboot_time)+' sec.')
	writefile(tmpf,str('restart'))
	sleep(reboot_time)
	while 1: sys.exit(0)

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
		logging.exception(' ['+timeadd(tuple(localtime()))+'] ')
		if debugmode:
			writefile(tmpf,str('exit'))
			raise


