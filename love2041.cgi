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

my @display_fields = ("name","gender", "height", "birthdate","weight", "degree", "favourite hobbies", "favourite books","favourite TV shows", "favourite movies", "favourite bands");


#attempting to run the program database.pl, setting up the connection to the database
$status = system("./database.pl");
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

#initialise the string that prints the html code
$page_html = "";

# print start of HTML ASAP to assist debugging if there is an error in the script
print &page_header();

$state = param('state') || "sign_in";

$page_html .= page_navbar();

if (param('search')){
	$page_html .= display_search();
}elsif ($state eq "profile"){
	$page_html .= display_profile();
} elsif ($state eq "sign_in"){
	$page_html .= page_title();
	$page_html .= page_sign_in();
} elsif ($state eq "browse") {
	$page_html .= display_users();
}


print "$page_html\n";

print &page_trailer();
exit 0;	

#function that displays all users.
sub display_users{
	my $html_code = "";
	my $n = param('n') || 0;

	if (defined(param('Prev')) || defined(param('Next'))){
		if(param('Prev')){
			$n -= 10;
		} elsif (param('Next')){
			$n += 10;
		}
	} else {
		$n = 0;
	}

	if ($n < 0){
		$n = 0;
	}

	my @students = glob("$students_dir/*");
	foreach my $student (@students){
		$student =~ s/\.\/students\///ig;
	}

	my $i = $n;
	param('n', $n);

	$html_code .= "<div class=\"container\" align=\"middle\">\n";
	$html_code .= "<div class=\"row\">\n";
	while ($i < $n+10){
		$stmt = qq(SELECT gender,birthdate, degree from USERS WHERE username="$students[$i]";);
	$sth = $dbh->prepare( $stmt );	
	$rv = $sth->execute() or die $DBI::errstr;
	if($rv < 0){
		print $DBI::errstr;
	}
	
	my @row = $sth->fetchrow_array();
	
	$html_code .= "<div class=\"panel panel-default\" style=\"width:400px\">\n";
	$html_code .= "  <div class=\"panel-heading\">\n";
	$html_code .= "     <div align=\"left\">\n";
	$html_code .= "	      <a href=\"love2041.cgi?state=profile&user=$students[$i]\"\n";
	$html_code .= "       <h2><b>$students[$i]</b></h2>\n";
	$html_code .= "       </a>\n";
	$html_code .= "		</div>\n";
	$html_code .= "  </div>\n";
	$html_code .= "  <center><img src=\"./students/$students[$i]/profile.jpg\"></centre>\n";
	$html_code .= "</div>\n";

		$i += 1;
	}	
	$html_code .= "</div>\n";
	$html_code .= "</div>\n";

	$html_code .= "<div class=\"row\">\n";
	$html_code .= "<div class=\"container\" align=\"middle\">\n";
#	param('n', $n);
 	$html_code .= p(
 		start_form, "\n",
		hidden('n', $n-10),"\n",
		hidden('n'),"\n",
		hidden('user'),"\n",
		hidden('prev'),"\n",
		hidden('next'),"\n",
 		submit('Prev'),"\n",
		end_form,"\n",
		start_form,"\n",
		hidden('n', $n),"\n",
 		submit('Next'),"\n",
 		end_form, "\n"
 	)."\n";
	$html_code .= "</div>\n";
	$html_code .= "</div>\n";

	return $html_code;

}


sub display_profile{
	my $html_code = "";
	my $n = param('n') || 0;
	my @students = glob("$students_dir/*");
	$n = min(max($n, 0), $#students);
	param('n', $n + 1);
	my $student_to_show = "";

	if (param('user')){
		$student_to_show = param('user');
	} else {
		$student_to_show  = $students[$n];
		$student_to_show =~ s/\.\/students\///ig;
	}

	$n += 1;
	$html_code.= " 
  <div class=\"row\">
	<div class=\"col-md-4\">
	  <div class=\"panel panel-default\" style=\"width:350px\">
        <div align=\"middle\" class=\"panel-heading\">
	      <h2><b><center>$student_to_show</center></b></h2></div>
            <div class=\"panel-body\">
              <center><img align=\"middle\" class=\"image rounded\" src=\"./students/$student_to_show/profile.jpg\"></center>
              <div align=\"right\">
     	        <p /><form method=\"post\" action=\"love2041.cgi\" enctype=\"multipart/form-data\">
                  <input type=\"submit\" name=\"state\" value=\"message\" />
<input type=\"hidden\" name=\"n\" value=\"$n\"  /></form>
                <p />
              </div>
	        </div>
        </div>
	  </div>
    </div>\n";


	$stmt = qq(SELECT name,gender, height, birthdate,weight, degree, favourite_hobbies, favourite_books,favourite_TV_shows, favourite_movies, favourite_bands from USERS WHERE username="$student_to_show";);
	$sth = $dbh->prepare( $stmt );	
	$rv = $sth->execute() or die $DBI::errstr;
	if($rv < 0){
		print $DBI::errstr;
	}
	
	my $index = 0;
	my @row = $sth->fetchrow_array();
	my $length = @row;
	my $profile = "";
	my $interest = "";
#	my @panel_info = ();
	while ($index < $length){
		if (defined($row[$index])){
			if ($row[$index] =~ /,@/ig){
				$row[$index] =~ s/,@/<p>\n<\/p>/ig;				
				$interest = $interest."<h5><b>".$display_fields[$index]."</b></h5>"."<ul>".$row[$index]."</ul>"."\n";
			} else {
				$profile = $profile."<h5><b>".$display_fields[$index]."</b></h5>"."<ul>".$row[$index]."</ul>"."\n";
			}
		}
		$index += 1;
	}
	
	$html_code.= "	<div class=\"col-md-4\">
    <div class=\"panel panel-primary\" style=\"width:500px\">
  	  <div class=\"panel-heading\">
        <h3 class=\"panel-title\">Interests</h3>
  	  </div>
      <div class=\"panel-body\">
	    <p class=\"text-info\">$profile</p>
  	  </div>
	</div>
	</div>
  </div>";


	$html_code.= "<div class=\"col-md-4\">
  <div class=\"panel panel-primary\" style=\"width:500px\">
  	<div class=\"panel-heading\">
      <h3 class=\"panel-title\">Personal Info</h3>
  	</div>
    <div class=\"panel-body\">
	  <p class=\"text-info\">$interest</p>
	</div>
  	</div>
  	</div>
  </div>";

	return $html_code;

}

sub display_search{
	my $html_code = "";
	my $search_string = param('search');
	@results = ();

	my @students = glob("$students_dir/*");
	foreach my $student (@students){
		$student =~ s/\.\/students\///ig;
		if ($student =~ /$search_string/i){
			push(@results, $student);
#			$html_code .= "<p><center>$student</center></p>\n";
		}
	}

	$html_code .= "<br><br>\n";
	if (!defined(@results)){
		$html_code .= "<center><h4 class=\"text-primary\">Sorry! There were no results found for <b>$search_string</b></h4></center>\n";
	} else {
		$html_code .= "<center><h4 class=\"text-primary\">Results for searching for <b>$search_string</b></h4></center>\n";
	}

	if (defined(@results)){

		$html_code .= "<div class=\"container\" align=\"middle\">\n";
		foreach $student (@results){

		$stmt = qq(SELECT gender, birthdate, degree from USERS WHERE username="$student";);
		$sth = $dbh->prepare( $stmt );	
		$rv = $sth->execute() or die $DBI::errstr;
		if($rv < 0){
			print $DBI::errstr;
		}
		
		my @row = $sth->fetchrow_array();
		$gender = $row[0];

			$html_code .= "<div class=\"panel panel-default\" style=\"width:700px\">\n";
			$html_code .= "  <div class=\"panel-heading\">\n";
			$html_code .= "	   <a href=\"love2041.cgi?state=profile&user=$student\"\n";
			$html_code .= "      <h3><b>$student</b></h3>\n";
			$html_code .= "    </a>\n";
			$html_code .= "  </div>\n";
			$html_code .= "  <div class=\"panel-body\">\n";
			$html_code .= "  <div style=\"float:left\">\n";
			$html_code .= "  <center><img src=\"./students/$student/profile.jpg\"></centre>\n";		
			$html_code .= "  </div>\n";
			$html_code .= "  <br><br>\n";
			$html_code .= "  <ul>\n";
			$html_code .= "    <p class=\"text-primary\">Gender: $row[0] </p>\n";
			$html_code .= "    <p class=\"text-primary\">Degree: $row[2] </p>\n";
			$html_code .= "  </ul>\n";
			$html_code .= "  </div>\n";
			$html_code .= "</div>\n";
		}
		$html_code .= "</div>\n";
	}
	return $html_code;
}


sub page_sign_in{
	my $html_code = "";

	open (F, "sign_in.txt") or die "cannot open navbar.txt";
	my @html_lines = <F>;
	my $html_code = "";
	foreach $line (@html_lines){
		$html_code = $html_code.$line;
	}
	close F;
	return $html_code;

}

sub authenticate{

	if (param('state')){
		if (param('state') eq "unauthenticated"){
			$html_code .= "<p><center>Username or password incorrect!</center></p>\n";
		}
	}
	if (param('Username') && param('Password')){
		$username = param('Username');
		$password = param('Password');
#		print "<p><center>$username</center></p>\n";
#		print "<p><center>$password</center></p>\n";

		my $stmt = qq(SELECT password from USERS WHERE username="$username";);
		$sth = $dbh->prepare( $stmt );	
		$rv = $sth->execute() or die $DBI::errstr;
		if($rv < 0){
			print $DBI::errstr;
		}

		my @row = $sth->fetchrow_array();

		if (defined(@row)){
			chomp($password);
			chomp($username);
			if ($password eq $row[0]){
				$state = "browse";
				param('state', $state);
				hidden('password');
			} else {
				$state = "unauthenticated";
				param('state', $state);	 
				hidden('password');
				#print "<p><center>Username or password incorrect!</center></p>\n";

			}
		} else {
			$state = "unauthenticated";
				param('state', $state);
				hidden('password');
			#print "<p><center>Username or password incorrect!</center></p>\n";
		}

	}
	return $state;

}

#
# HTML placed at bottom of every screen
#

sub page_navbar{

	open (F, "navbar.txt") or die "cannot open navbar.txt";
	my @html_lines = <F>;
	my $html_code = "";
	foreach $line (@html_lines){
		$html_code = $html_code.$line;
	}

	close F;
	return $html_code;
}


sub page_title{
	open (F, "title.txt") or die "cannot open navbar.txt";
	@html_lines = <F>;
	$html_code = "";
	foreach $line (@html_lines){
		$html_code = $html_code.$line;
	}
	close F;
	return $html_code;
}


sub page_header {
	return header,
   		start_html(
		-style=>{'-src'=>"//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/yeti/bootstrap.min.css"}, "-title"=>"UNSW LOVE2041");
#	header,"\n";	
	
}

# HTML placed at bottom of every screen
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
	my $html = "";
	$html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
	
	#$html .= end_html;
	$html .= "<script src=\"http://code.jquery.com/jquery.min.js\"></script>\n";
	$html .= "<script src=\"js/bootstrap.min.js\"></script>\n";

	$html .= end_html;
	return $html;
}
