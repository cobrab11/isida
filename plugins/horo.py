#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author ferym

import urllib2,re
import string


global horodb
horodb={u'овен': u'/aries/today', u'телец': u'/taurus/today', u'близнецы': u'/gemini/today', u'рак': u'/cancer/today', u'лев': u'/leo/today', u'дева': u'/virgo/today', u'весы': u'/libra/today', u'скорпион': u'/scorpio/today', u'стрелец': u'/sagittarius/today', u'козерог': u'/capricorn/today', u'водолей': u'/aquarius/today', u'рыбы':u'/pisces/today'}

def handler_horoscope(type, jid, nick, parameters):
  if parameters:
    if parameters==u'list':
      zod = [u'Овен', u'Телец', u'Близнецы', u'Рак', u'Лев', u'Дева', u'Весы', u'Скорпион', u'Стрелец', u'Козерог', u'Водолей', u'Рыбы']
      send_msg(type, jid, nick, ', '.join(zod))
      return
    if parameters==u'date':
      date = [u'Овен (21.03-19.04)', u'Телец (20.04-20.05)', u'Близнецы (21.05-20.06)', u'Рак (21.06-22.07)', u'Лев (23.07-22.08)', u'Дева (23.08-22.09)', u'Весы (23.09-22.10)', u'Скорпион (23.10-21.11)', u'Стрелец (22.11-21.12)', u'Козерог (22.12-19.01)', u'Водолей (20.01-18.02)', u'Рыбы (19.02-20.03)']
      sp = ''
      nm = 1
      for tb in date:
        sp+=str(nm)+'. '+tb+u'\n'
        nm+=1
      if type=='groupchat':
        send_msg(type, jid, nick, u'ушёл в приват')
        send_msg('chat', jid, nick, u'Список дат:\n'+sp)
        return 
      send_msg('chat', jid, nick, u'Список дат:\n'+sp)
      return
    if horodb.has_key(parameters.lower()):
      req = urllib2.Request('http://horo.mail.ru/prediction'+horodb[parameters.lower()])
      req.add_header = ('User-agent', 'Mozilla/5.0')
      r = urllib2.urlopen(req)
      target = html_encode(r.read())
      od = re.search('<div id="tm_today">',target)
      message = target[od.end():]
      message = message[:re.search('<script type="text/javascript">',message).start()]
      message = rss_del_html(message)
      message = rss_del_nn(message)
      message = rss_replace(message)
      message = message.replace('\n','')
      if type=='groupchat':
          send_msg(type,jid,nick,u'ушёл в приват')
          send_msg('chat',jid,nick,message)
          return
      send_msg('chat',jid,nick,message)
    else:
      send_msg(type, jid, nick, u'что это за знак зодиака?')	
      return	
  else:
    send_msg(type,jid,nick,u'для какого знака гороскоп смотреть-то?')
    return


global execute

execute = [(0, u'horo', handler_horoscope, 2, u'Показывает гороскоп для указанного знака гороскопа. Просмотр знаков зодиака - "horo list". Просмотр списка дат - "horo date" | Author: ferym')]