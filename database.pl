#!/usr/bin/perl -w

#perl program used to initialise the database via Sqlite3. This is to be used to set up 
#the database before running the CGI program to open the link.
#This program will open a connection to a database, using SQL, it will insert in information
#that is retrieved from the students folder profile and add it to the database
#It will then save the changes to the database and close before running the cgi program

use DBI;
use strict;

#setting up the connection to the database, or initialising if the table is not created

my $driver   = "SQLite"; 
my $database = "test.db";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";
my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 }) 
                      or die $DBI::errstr;

print "Opened database successfully\n";

#creating a new table and setting the fields
my $stmt = qq(CREATE TABLE USERS
      (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       username       TEXT    NOT NULL,
       password       TEXT	  NOT NULL
      ););
my $rv = $dbh->do($stmt);
if($rv < 0){
   print $DBI::errstr;
} else {
   print "Table created successfully\n";
}

#opening up all the usernames in students folder. 
opendir my $students_folder, 'students' or die "couldn't open folder students";

my @folders = readdir $students_folder;

foreach my $user (@folders){
	print "$user\n";
}
closedir $students_folder;

$dbh->disconnect();