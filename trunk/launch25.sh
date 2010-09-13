#!/bin/sh

rm -f plugins/list.txt
svn up
python2.5 isida.py
