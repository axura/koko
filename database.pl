#!/usr/bin/perl -w

#perl program used to initialise the database via Sqlite3. This is to be used to set up 
#the database before running the CGI program to open the link.
#This program will open a connection to a database, using SQL, it will insert in information
#that is retrieved from the students folder profile and add it to the database
#It will then save the changes to the database and close before running the cgi program
#printing functions for debugging purposes and for checking the status have been commented out

use DBI;

#setting up the connection to the database, or initialising if the table is not created
#the following if statement checks if the database exists, if so will return so datbase
#will not need to be created again.
if (-e "students.db"){
	#print "database already exists. No need to initialise\n";
	exit(0);
}

my $driver   = "SQLite"; 
my $database = "students.db";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";
my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 }) 
                      or die $DBI::errstr;

#print "Opened database successfully\n";

#creating a new table and setting the fields. All data is stored in a large table
my $stmt = qq(CREATE TABLE USERS
      (ID INT PRIMARY KEY,
       name           				TEXT,
       username       				TEXT,
       password       				TEXT,
	   degree		  				TEXT,
       height         				TEXT,
       birthdate      				TEXT,
       favourite_hobbies        	TEXT,
       weight           			TEXT,
       favourite_TV_shows           TEXT,
       favourite_movies			    TEXT,
       email           				TEXT,
       courses           			TEXT,
       gender           			TEXT,
       hair_colour          		TEXT,
       favourite_books           	TEXT,
	   favourite_bands				TEXT
      ););
my $rv = $dbh->do($stmt);
if($rv < 0){
   print $DBI::errstr;
} #else {
  # print "Table created successfully\n";
#}

$stmt = qq(CREATE TABLE PREFERENCES
      (ID INT PRIMARY KEY,
       username       				TEXT,
       height_min         			TEXT,
       height_max      				TEXT,
       weight           			TEXT,
       gender           			TEXT,
       hair_colours          		TEXT,
       age_min			           	TEXT,
	   age_max						TEXT
      ););
$rv = $dbh->do($stmt);
if($rv < 0){
   print $DBI::errstr;
} else {
   print "Table PREFERENCES created successfully\n";
}

#opening up all the usernames in students folder. 
opendir $students_folder, 'students' or die "couldn't open folder students";

@folders = readdir $students_folder;


#function when reading a multiline field. The function will concat all the items into a single
#string, separated by ",@" characters, as they are not commonly used together. 
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


sub preferences{
	my $entry = $line;
	my $index = $file_index + 1;
	
	return $entry;
}

#hashtable used for checking the entries that require min and max
%min_max_fields = (
	"height" => "height",
	"weight" => "weight",
	"age"	 =>	"age",
);

#with the list of users given from the folder names. it will traverse through each folder, 
#loop will open the profile.txt in each file, to read for the fields. 
#Once it has found a new field, it will call the function to set the items as a string


foreach $user (@folders){
	#check if it is a valid username, otherwise go to next folder
	if ($user =~ /^[^a-z0-9].*$/ig){
		next;
	}

	%table_entries = ();
	$file_location = "students/".$user."/profile.txt";
	#strings passed into the insert instruciton for SQL
	@fields = ();
	@values = ();

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
		if (defined($curr_field) && defined($insert_field)){
			$table_entries{$curr_field} = $insert_field;
			push(@fields, $curr_field);
			push(@values, $insert_field);
#			printf "%s: %s\n", $curr_field, $table_entries{$curr_field};			
		}
		$file_index += 1;
		$curr_field = undef;
		$insert_field = undef;
	}

		#inserting information for that user into the sqlite3 table

		$id_string = join(",", @fields);
		$value_string = join("', '", @values);
		$value_string = "'".$value_string."'";	
		$stmt = qq(INSERT INTO USERS ($id_string) VALUES ($value_string ););
		$rv = $dbh->do($stmt) or die $DBI::errstr;
	
		
#printf "%s: %s\n", $id_string, $value_string;
	close(File);

	%pre_entries = ();
	$file_location = "students/".$user."/preferences.txt";
	#strings passed into the insert instruciton for SQL
	@fields = ();
	@values = ();

	open(File, "$file_location") or die "cannot open the profile text for $user\n";
	@lines = <File>;
	$length = @lines;
	$file_index = 0;
	foreach $line (@lines){
		if($line =~ /^([_a-z].*)/i){
			$curr_field = $1;
			$curr_field =~ s/:\s*$//ig;

			if (!defined($min_max_fields{$curr_field})){
				$insert_field = &multiItemfield();			
#				print "$user: $curr_field - $insert_field\n";
			} else {
				my $field_range = $curr_field;
				print "$user: $field_range\n";
			}
		}

		if (defined($curr_field) && defined($insert_field)){
			$pre_entries{$curr_field} = $insert_field;
			push(@fields, $curr_field);
			push(@fields, $insert_field);
		}

		$file_index += 1;
		$curr_field = undef;
		$insert_field = undef;
			
	}
		
	close File;	

}

#closing all directories and saving creation.

#print "inserted all of the information from profiles without problems\n";
closedir $students_folder;

$dbh->disconnect();
exit(0);
