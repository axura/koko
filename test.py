#!/usr/bin/python

#code structure for initialising SQLite
import sqlite3
import os

"""step 1 make connection
seems to be a single file, does this mean that we would need to 
append all the data to a file first?
"""
conn = sqlite3.connect('students.db')
os.gedcwd()


#step 2 setting up the fields
cursor = conn.cursor()

sql = "%CREATE TABLE Users(id INTEGER PRIMARY KEY, AUTOINCREMENT,
	name TEXT,
	degree	TEXT,
	password TEXT,
	height	FLOAT,

	#etc etc
	username TEXT)
#step 3. add in fields

cursor.execute() #not sure what to add in here

print (cursor.description)


#step 4 insert in the data. in the VALUES parenthesis, addd in the field values
#do this for each individual file
sql = "INSERT INTO Users(name, degree, password, height... ,username) VALUES ())"

#step 5
cursor.execute(sql)

conn.commit()

