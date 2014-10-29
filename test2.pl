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

my $stmt = qq(SELECT username from USERS);
my @user_column = ();

my $sth = $dbh->prepare( $stmt );	
	my $rv = $sth->execute() or die $DBI::errstr;
	if($rv < 0){
		print $DBI::errstr;
	}
	@user_column=$sth->fetchall_arrayref();

	my $student = "GeekGirl42"; 

	print "----------------------------$student------------------------------\n";

	$stmt = qq(SELECT name,gender, height, birthdate,weight, degree, favourite_hobbies, favourite_books,favourite_TV_shows, favourite_movies, favourite_bands from USERS WHERE username="$student";);
	$sth = $dbh->prepare( $stmt );	
	$rv = $sth->execute() or die $DBI::errstr;
	if($rv < 0){
		print $DBI::errstr;
	}

	my $index = 0;
	my @row = $sth->fetchrow_array();
	my $length = @row;
	my $profile = "";
	while ($index < $length){
		if (defined($row[$index])){
			$row[$index] =~ s/,@/\n/ig;
			$profile =$profile.$row[$index]."\n";
		}
		$index += 1;
	}
	print "$profile";


	
