#!/usr/bin/python

#file for initialising database
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

match = re.search("username:\n", file_strings)

if match:
	print match.group()


f.close()


#save what was created
conn.commit()
