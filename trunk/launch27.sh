#!/bin/sh

rm -f plugins/list.txt
svn up
python2.7 isida.py