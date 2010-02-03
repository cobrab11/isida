short howto for isida-bot

- installation -

no need. download by svn in any folder from official repository by:
svn co http://isida.googlecode.com/svn/trunk isida

- launch -

1. rename defaul_config.py to config.py and fill look inside
2. create startup databases with "python create_databases.py" command
3. type in console: sh launch.sh for launch with defaul python version or sh launch26.sh for launch with python 2.6 (recomended)

- update -

after global bot update - launch "sh update" script for correct update.


- fast install and launch -

svn co http://isida.googlecode.com/svn/trunk isida
cd isida/settings
cp demo_config.py config.py
nano config.py
cd ..
sh launch26.sh &

that's all :)

(c) Disabler Producion Lab.
