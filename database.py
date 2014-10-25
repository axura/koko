#!/usr/bin/python

#file for initialising database using SQlite
import sqlite3
import os
import re
import glob

#make connection
conn = sqlite3.connect('students.db')
#os.gedcwd()

#step 2 setting up the fields
cursor = conn.cursor()

f = open("students/CrazyNinja82/profile.txt", "r")
#print f.read()
file_strings = str(f.read())
print file_strings
user_pattern = "username:\n\t[a-z0-9s\.]*"
password_pattern = "password:\n\t[a-z0-9s\.]*"
name_pattern = "name:\n\t[a-z0-9s\.]*"

match = re.search(user_pattern, file_strings,re.IGNORECASE)
name_match = re.search(name_pattern, file_strings, re.IGNORECASE)
pass_match = re.search(password_pattern, file_strings,re.IGNORECASE)
print
print "found the following"
if match:
	print name_match.group()
	print match.group()
	print pass_match.group()
f.close()

#creating user table

sql = """CREATE TABLE Users(id INTEGER PRIMARY KEY,
	name	TEXT, 
	username TEXT,
	password TEXT)
	"""
#cursor.execute(sql)

#cursor.execute('select * from Users')
 
sql = "INSERT INTO Users(name, username, password) VALUES (name_match.group(), match.group(), pass_match.group()))"


#save what was created
conn.commit()
