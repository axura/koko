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
      (ID INT PRIMARY KEY,
       name           TEXT,
       username       TEXT,
       password       TEXT,
	   degree		  TEXT,
       height           TEXT,
       birthdate           TEXT,
       favourite_hobbies           TEXT,
       weight           TEXT,
       favourite_TV_shows           TEXT,
       favourite_movies     TEXT,
       email           TEXT,
       courses           TEXT,
       gender           TEXT    ,
       hair_colour           TEXT,
       favourite_books           TEXT
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
	my @items = ();
	my $index = $file_index+1;
	$listOfEntries = "";
#	print "$index, $length, $line";
	while (($index < $length) && ($lines[$index] =~ /^\t/i)){
		$entry = $lines[$index];
		chomp($entry);
		$entry =~ s/^\s*//i;
		$entry =~ s/'/\&\#8216/ig;
		push(@items, $entry);
		$index += 1;
	}
	$listOfEntries = join(",@", @items);
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
			print "$curr_field: $insert_field\n";
		}
		if (defined($curr_field) && defined($insert_field)){
			$table_entries{$curr_field} = $insert_field;
#			$stmt = qq(INSERT INTO USERS ($curr_field) VALUES ($insert_field ););
#			$rv = $dbh->do($stmt) or die $DBI::errstr;

		}	
		$file_index += 1;
		$curr_field = undef;
		$insert_field = undef;
	}

	close(File);

	#inserting information for that user into the sqlite3 table
}
closedir $students_folder;

$dbh->disconnect();
