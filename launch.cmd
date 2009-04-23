# update to actual version
svn up

#copy version to file
echo `svnversion` > version

#launch bot
python isida.py