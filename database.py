#!/usr/bin/python

#file for initialising database
import sqlite3
import os
import re

#make connection
conn = sqlite3.connect('students.db')
#os.gedcwd()


#save what was created
conn.commit()
