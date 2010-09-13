#!/bin/sh

rm -f plugins/list.txt
svn up
python2.6 isida.py