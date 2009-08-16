#!/bin/sh
# update to actual version
rm plugins/list.txt
svn up

#copy version to file
echo `svnversion` > settings/version

#launch bot
python2.6 start.py
