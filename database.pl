#!/usr/bin/perl -w

#perl program used to initialise the database via Sqlite3. This is to be used to set up 
#the database before running the CGI program to open the link.
#This program will open a connection to a database, using SQL, it will insert in information
#that is retrieved from the students folder profile and add it to the database
#It will then save the changes to the database and close before running the cgi program

use DBI;
#use strict;

#setting up the connection to the database, or initialising if the table is not created

my $driver   = "SQLite"; 
my $database = "test.db";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";
my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 }) 
                      or die $DBI::errstr;

#print "Opened database successfully\n";

#creating a new table and setting the fields
my $stmt = qq(CREATE TABLE USERS
      (ID INT PRIMARY KEY     NOT NULL,
       name           TEXT    NOT NULL,
       username       TEXT    NOT NULL,
       password       TEXT	NOT NULL,
	   degree			TEXT	NOT NULL,
       height           TEXT    NOT NULL,
       birthdate           TEXT    NOT NULL,
       favourite_hobbies           TEXT    NOT NULL,
       weight           TEXT    NOT NULL,
       favourite_TV_shows           TEXT    NOT NULL,
       favourite_movies     TEXT    NOT NULL,
       email           TEXT    NOT NULL,
       courses           TEXT    NOT NULL,
       gender           TEXT    NOT NULL,
       hair_colour           TEXT    NOT NULL,
       favourite_books           TEXT    NOT NULL
      ););
my $rv = $dbh->do($stmt);
if($rv < 0){
   print $DBI::errstr;
} else {
   print "Table created successfully\n";
}

#opening up all the usernames in students folder. 
opendir $students_folder, 'students' or die "couldn't open folder students";

@folders = readdir $students_folder;

sub multiItemfield{
	my $entry = $line;
	my @items = [];
	my $index = $file_index+1;
	$listOfEntries = "";
#	print "$index, $length, $line";
	while (($index < $length) && ($lines[$index] =~ /^\t/i)){
		$entry = $lines[$index];
		chomp($entry);
		$entry =~ s/^\s*//i;
		push(@items, $entry);
		if ($index != ($file_index +1)){
			$listOfEntries = $listOfEntries.',@'.$entry;
		} else {
			$listOfEntries = $entry;
		}
		$index += 1;
	}
	
	return $listOfEntries;
}

foreach $user (@folders){
	#check if it is a valid username, otherwise go to next folder
	if ($user =~ /^[^a-z0-9].*$/ig){
		next;
	}
#	@insert = [];
	%table_entries = ();
	$file_location = "students/".$user."/profile.txt";

	open(File, "$file_location") or die "cannot open the profile text for $user\n";
	@lines = <File>;
	$length = @lines;
	$file_index = 0;
	foreach $line (@lines){
		if (($line =~ /^([_a-z].*):$/i) || ($line =~ /favourite/i)) {
			$insert_field = &multiItemfield();
			$curr_field = $1;
#			print "$curr_field: $insert_field\n";
		}

		$table_entries{$curr_field} = $insert_field;
		$file_index += 1;
	}

	close(File);

}
closedir $students_folder;

$dbh->disconnect();
