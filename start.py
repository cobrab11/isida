#!/usr/bin/python
# -*- coding: utf -*-

import os

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

while 1:
    try:
        execfile('isida.py')
    except Exception, SM:
        if os.path.isfile('tmp'):
            mode = str(readfile('tmp'))
            if mode == 'exit':
                os._exit(0)
            
