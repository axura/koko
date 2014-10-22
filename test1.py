#!/usr/bin/python

#test file for initialising database called "test.db"

import sqlite3

conn = sqlite3.connect('test.db')
print "opened database successfully"

conn.execute('''CREATE TABLE USERS
	(ID INT PRIMARY KEY	NOT NULL,
	name		TEXT	NOT NULL,
	username	TEXT	NOT NULL,
	password	TEXT	NOT NULL);''')

print "Table Users created successfully"

conn.execute("INSERT INTO USERS (IO, name, username, password) \ VALUES (Ninja, teh1994, teh1994panda)")

conn.commit()

conn.close()
