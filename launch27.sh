#!/bin/sh

if [ -e plugins/list.txt ] ; then rm -f plugins/list.txt.back && mv plugins/list.txt.back plugins/list.txt ; fi
svn up
if [ ! -e plugins/list.txt ] ; then mv plugins/list.txt.back plugins/list.txt ; fi
python2.7 isida.py