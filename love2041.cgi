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


#attempting to run the program database.pl, setting up the connection to the database
$status = system("./database.pl");

# print start of HTML ASAP to assist debugging if there is an error in the script
print page_header();
my $driver   = "SQLite";
my $database = "students.db";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";
my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 })
                      or die $DBI::errstr;

# some globals used through the script
$debug = 1;
$students_dir = "./students";

&show_profile();

print page_trailer();
exit 0;	

sub browse_screen {
	my $n = param('n') || 0;
	my @students = glob("$students_dir/*");
	$n = min(max($n, 0), $#students);
	param('n', $n + 1);
	my $student_to_show  = $students[$n];
	my $profile_filename = "$student_to_show/profile.txt";
	open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
	$profile = join '', <$p>;
	close $p;
	
	return p,
		start_form, "\n",
		pre($profile),"\n",
		hidden('n', $n + 1),"\n",
		submit('Next student'),"\n",
		end_form, "\n",
		p, "\n";
}

sub show_profile{
	open (F, "navbar.txt") or die "cannot open navbar.txt";
	my @html_lines = <F>;
	my $html_code = "";
	foreach $line (@html_lines){
		$html_code = $html_code.$line;
	}

	print "$html_code";
	close F;

	my $display_profile = &display_profile();
	print "	<div class=\"panel panel-primary\">
  	<div class=\"panel-heading\">
      <h3 class=\"panel-title\">Personal Info</h3>
  	</div>
    <div class=\"panel-body\">
	  <p class=\"text-info\">$display_profile</p>
  	</div>
  </div>";
	#print "<p class=\"text-info\">$display_profile</p>\n";

}

#function that displays all users.
sub display_users{
	#$n

}


sub display_profile{
	my $n = param('n') || 0;
	my @students = glob("$students_dir/*");
	$n = min(max($n, 0), $#students);
	param('n', $n + 1);
	my $student_to_show  = $students[$n];
	$student_to_show =~ s/\.\/students\///ig;

	print "  <div class=\"panel panel-default\" style=\"width:350px\">
    <div align=\"middle\" class=\"panel-heading\">
	  <h2><b><center>$student_to_show</center></b></h2></div>
      <div class=\"panel-body\">
        <center><img align=\"middle\" class=\"image rounded\" src=\"./students/$student_to_show/profile.jpg\"></center>
      </div>
    </div>
  </div>\n";


	$stmt = qq(SELECT name,gender, height, birthdate,weight, degree, favourite_hobbies, favourite_books,favourite_TV_shows, favourite_movies, favourite_bands from USERS WHERE username="$student_to_show";);
	$sth = $dbh->prepare( $stmt );	
	$rv = $sth->execute() or die $DBI::errstr;
	if($rv < 0){
		print $DBI::errstr;
	}
	
	print p,
		start_form,"\n",
		submit("Message"),"\n",
		hidden('n', $n + 1),
		end_form,"\n",
		p,"\n";

	my $index = 0;
	my @row = $sth->fetchrow_array();
	my $length = @row;
	my $profile = "";
	while ($index < $length){
		if (defined($row[$index])){
			if ($row[$index] =~ /,@/ig){
				$row[$index] =~ s/,@/<p>\n<\/p>/ig;
				$profile = $profile."<h4><b>".$display_fields[$index]."</b></h4>"."<ul>".$row[$index]."</ul>"."\n";
			} else {
				$profile = $profile."<h4>".$display_fields[$index]."</h4>"."<ul>".$row[$index]."</ul>"."\n";
			}
		}
		$index += 1;
	}

	return $profile;
}



#
# HTML placed at bottom of every screen
#
sub page_header {
	print header,
   		start_html(
		-style=>{'-src'=>"//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/yeti/bootstrap.min.css"}, "-title"=>"UNSW LOVE2041");

}

# HTML placed at bottom of every screen
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
	my $html = "";
	$html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
	
	#$html .= end_html;
	print "<script src=\"http://code.jquery.com/jquery.min.js\"></script>\n";
	print "<script src=\"js/bootstrap.min.js\"></script>\n";

	$html .= end_html;
	return $html;
}
