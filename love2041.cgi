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
	print "    <div class=\"navbar navbar-inverse navbar-fixed-top\" role=\"navigation\">
      <div class=\"container\">
        <div class=\"navbar-header\">
          <button type=\"button\" class=\"navbar-toggle collapsed\" data-toggle=\"collapse\" data-target=\"#navbar\" aria-expanded=\"false\" aria-controls=\"navbar\">
            <span class=\"sr-only\">Toggle navigation</span>
            <span class=\"icon-bar\"></span>
            <span class=\"icon-bar\"></span>
            <span class=\"icon-bar\"></span>
          </button>
          <a class=\"navbar-brand\" href=\"#\">Project name</a>
        </div>
        <div id=\"navbar\" class=\"collapse navbar-collapse\">
          <ul class=\"nav navbar-nav\">
            <li class=\"active\"><a href=\"#\">Home</a></li>
            <li><a href=\"#about\">About</a></li>
            <li><a href=\"#contact\">Contact</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>\n";
#	print "<div class=\"jumbotron\"><div class=\"container\">\n";
	my $display_profile = &display_profile();
	print "<p>$display_profile</p>\n";
#	print "</div>\n";
}

sub display_profile{
	my $n = param('n') || 0;
	my @students = glob("$students_dir/*");
	$n = min(max($n, 0), $#students);
	param('n', $n + 1);
	my $student_to_show  = $students[$n];
	$student_to_show =~ s/\.\/students\///ig;

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
				$profile = $profile."<h3>".$display_fields[$index]."</h3>"."<ul>".$row[$index]."</ul>"."\n";
			} else {
				$profile = $profile."<h3>".$display_fields[$index]."</h3>"."<ul>".$row[$index]."</ul>"."\n";
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
   		start_html("-title"=>"UNSW LOVE2041"); #-bgcolor=>"#B0E0E6");
		print "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n";
    	print "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/bootstrap.min.css\">\n";
		#print "<title>UNSW 2041 Friend searcher</title>";
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
#	print "  <script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js\"></script>
#    <script src=\"../../dist/js/bootstrap.min.js\"></script>
#    <script src=\"../../assets/js/ie10-viewport-bug-workaround.js\"></script>";
	$html .= end_html;
	return $html;
}
