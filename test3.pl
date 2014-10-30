#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2013
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/LOVE2041/

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
use DBI;
warningsToBrowser(1);

my @display_fields = ("name","gender", "height", "birthdate","weight", "degree", "favourite_hobbies", "favourite_books","favourite_TV_shows", "favourite_movies", "favourite_bands");

my $driver   = "SQLite";
my $database = "students.db";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";
my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 })
                      or die $DBI::errstr;

my @students = glob("$students_dir/*");

for my $student (@students){
	$student =~ s/.\/students\///ig;
	print $student,"\n";
}

open (F, "navbar.txt") or die "cannot open navbar.txt";
my @html_lines = <F>;
my $html_code = "";
foreach $line (@html_lines){
	$html_code = $html_code.$line."\n";
}

print "\npriting html code ---------------------------------\n";
print "$html_code\n";
