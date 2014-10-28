#!/usr/bin/perl -w

#test file for checking for displaying profile and extracting from database.

use DBI;
use strict;

my $status = system("./database.pl");

my $driver   = "SQLite";
my $database = "students.db";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";
my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 })
                      or die $DBI::errstr;
print "Opened database successfully\n";

my $stmt = qq(SELECT username, name,gender, height, birthdate,weight, degree, favourite_hobbies, favourite_books,favourite_TV_shows, favourite_movies, favourite_bands  from USERS;);
	my $sth = $dbh->prepare( $stmt );	
	my $rv = $sth->execute() or die $DBI::errstr;
	if($rv < 0){
		print $DBI::errstr;
	}
	
	my $index = 0;
	my @row = $sth->fetchrow_array();
	my $length = @row;
	foreach my $entry (@row){	
		$index = 0;
		while ($index < $length){
			if (defined($row[$index])){
				$row[$index] =~ s/,@/\n/ig;
				print "$index: $row[$index]\n";
			}
		$index +=1;
		}
	}


	
