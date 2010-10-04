#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
	Python implementation of Haversine formula
	Copyright (C) <2009>	Bartek GГіrny <bartek@gorny.edu.pl>
"""

import math

def recalculate_coordinate(val,	_as=None):
	deg,	min,	sec = val
	# pass outstanding values from right to left
	min = (min or 0) + int(sec) / 60
	sec = sec % 60
	deg = (deg or 0) + int(min) / 60
	min = min % 60
	# pass decimal part from left to right
	dfrac,	dint = math.modf(deg)
	min = min + dfrac * 60
	deg = dint
	mfrac,	mint = math.modf(min)
	sec = sec + mfrac * 60
	min = mint
	if _as:
		sec = sec + min * 60 + deg * 3600
		if _as == 'sec': return sec
		if _as == 'min': return sec / 60
		if _as == 'deg': return sec / 3600
	return deg,	min,	sec
  
def points2distance(start,	end):
	"""
		Calculate distance (in kilometers) between two points given as (long, latt) pairs
		based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula).
	"""
	start_long = math.radians(recalculate_coordinate(start[0],	'deg'))
	start_latt = math.radians(recalculate_coordinate(start[1],	'deg'))
	end_long = math.radians(recalculate_coordinate(end[0],	'deg'))
	end_latt = math.radians(recalculate_coordinate(end[1],	'deg'))
	d_latt = end_latt - start_latt
	a = (math.cos(end_long) * math.sin(d_latt))**2 + (math.cos(start_long)*math.sin(end_long)-math.sin(start_long)*math.cos(end_long)*math.cos(d_latt))**2
	b = math.sin(start_long)*math.sin(end_long) + math.cos(start_long)*math.cos(end_long)*math.cos(d_latt)
	dist = math.atan2(math.sqrt(a), b) * 6372.795
	dist = str(dist).split('.')[0]
	return dist

def dist(type, jid, nick, text):
	parameters = text.strip()
	geodict = eval(readfile('plugins/dist.txt').decode('utf-8'))
	if " - " in parameters:
		towns = parameters.strip().split(" - ")
	else:
		towns = parameters.strip().split()
	if len(towns)==2 and geodict.has_key(towns[0].lower()) and geodict.has_key(towns[1].lower()):
		t1 = map(int, geodict[towns[0].lower()].split())
		t2 = map(int, geodict[towns[1].lower()].split())
		distance = points2distance(((t1[0], t1[1], 0),	(t1[2], t1[3], 0)), ((t2[0], t2[1], 0),	(t2[2], t2[3], 0)))
		msg = u"%s километров" % distance
	else:
		msg = L('What?')
	send_msg(type,jid,nick,msg)


global execute

execute = [(3, 'dist', dist, 2, L('Distance between cities'))]
