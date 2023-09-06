#!/usr/bin/env bash

# change directory to the location of this script
cd $(dirname $0)

#load strings from python config... this is probably pretty brittle, but it works as long as we keep the config really minimal
source config.py

# initialize empty databases
if ! [ -f $ACCOUNTS_DB ]
then
	echo 'run setup.sh first' > /dev/stderr
	exit 1
fi

sqlite3 $ACCOUNTS_DB "SELECT username FROM accounts;"
