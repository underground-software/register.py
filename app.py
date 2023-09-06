#!/usr/bin/env python3
import sqlite3
from urllib.parse import parse_qs
from html import escape
from config import *
from orbit import appver, messageblock, ROOT, DP

FIND_ACCOUNT_QUERY='''\
SELECT
	a.id,
	a.username,
	a.password
FROM
	accounts a
WHERE
	a.student_id = '%s'
;
'''

DELETE_ACCOUNT_QUERY='''\
DELETE FROM
	accounts
WHERE
	id = %d
;
'''

def accounts_db_exec(command, commit=False):
	con = sqlite3.connect(ACCOUNTS_DB)
	cur = con.cursor()
	cur2 = cur.execute(command)
	res = cur2.fetchall()
	if commit:
		con.commit()
	con.close()
	return res

def handle_post_request(env, start_response):
	form_data = parse_qs(env['wsgi.input'].read(int(env['CONTENT_LENGTH'])))
	print(form_data)
	if b'student_id' not in form_data or len(form_data[b'student_id']) != 1:
		start_response('400 Bad Request', [('Content-Type', 'text/html')])
		return '<h1>Bad Request</h1><br>\n'
	result = accounts_db_exec(FIND_ACCOUNT_QUERY % escape(str(form_data[b'student_id'][0],'utf-8')))
	if not result:
		start_response('200 OK', [('Content-Type', 'text/html')])
		return '<h1>No such user</h1><br>\n'
	((id, username, password),) = result
	accounts_db_exec(DELETE_ACCOUNT_QUERY % id, commit=True)
	start_response('200 OK', [('Content-Type', 'text/html')])
	return f'''\
	<h1>Save these credentials, you will not be able to access them again</h1><br>
	<h3>Username: {username}</h1><br>
	<h3>Password: {password}</h1><br>
	'''

def application(env, start_response):
	with open(ROOT + '/data/header') as header:
		page = header.read();
	#only set for post request
	if 'CONTENT_LENGTH' in env and env['CONTENT_LENGTH']:
		page += handle_post_request(env, start_response)
	else:
		page += '''\
		<form id="register" method="post" action="/register">
			<label for="student_id">Student ID:</label>
			<input name="student_id" type="text" id="student_id" /><br />
			<button type="submit">Submit</button>
		</form>
		'''
		start_response('200 OK', [('Content-Type', 'text/html')])
	page += messageblock([('appver', appver())])
	return bytes(page, 'UTF-8')

