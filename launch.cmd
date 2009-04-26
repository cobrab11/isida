# update to actual version
svn up

#copy version to file
echo `svnversion` > settings\version

#launch bot
python start.py