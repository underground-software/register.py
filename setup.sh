#!/bin/bash

# basic setup of auth server

# change directory to the location of this script
cd $(dirname $0)

#load strings from python config... this is probably pretty brittle, but it works as long as we keep the config really minimal
source config.py

# initialize empty databases
[ -f $ACCOUNTS_DB ] || sqlite3 $ACCOUNTS_DB 'CREATE TABLE accounts (id INTEGER PRIMARY KEY, student_id STRING UNIQUE NOT NULL, username STRING NOT NULL, password STRING NOT NULL);'

# install python dependencies
pip install -r requirements.txt
