#!/usr/bin/perl -w

#written by Yue (Alice) Kang
#dating website "UNSW 2041 Friend Searcher"


use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
use DBI;
warningsToBrowser(1);

#array of information fields, to be used for the display profiles
my @display_fields = ("name","gender", "height", "birthdate","weight", "degree", "favourite hobbies", "favourite books","favourite TV shows", "favourite movies", "favourite bands");

#attempting to run the program database.pl
$status = system("./database.pl");

#setting connection to the database "students.db"
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
$page_title = "";
$page_html = "";

# print start of HTML ASAP to assist debugging if there is an error in the script
print &page_header();

$state = param('state') || "sign_in";

$unsigned = 1;

#checks for the cases of what page is accessed.
#it checks for the following cases: scrolling through browsed users, logging in a user
#login error, reading profile, sign in page. It calls the relevant functions to concat the
#html code relevant to a string before printing it. Afterwards the page_trailer is printed
if (param('Next') || param('Prev')){
	$page_html .= display_users();
	$unsigned = 0;
} elsif (param('Username') && param('Password')){
		$login = &authenticate();
		if ($login == 1){
			$page_html .= login();
			$unsigned = 0;
		} else {
			$page_html .= login_error();
			$error = 1;
		}
}

if ($unsigned == 1){
	$page_title = page_navbar();
} else {
	$page_title = page_navbar_login();
}
	$page_html = $page_title.$page_html;

if ($unsigned == 1 && $error == 0){
	if (param('search')){
		$page_html .= display_search();
	} elsif ($state eq "profile"){
		$page_html .= display_profile();
	} elsif ($state eq "browse") {
		$page_html .= display_users();
	} elsif ($state eq "sign_in"){
		$page_html .= page_title();
		$page_html .= page_sign_in();
	}
}


print "$page_html\n";

print &page_trailer();
#exit 0;	

#writes the html code for the welcome page after a user logs in
#in addition, the function will also find any matching users for the current user
#the set of users will be used to call display_matches(), used to display the results
#directly underneath the welcome title
sub login{
	my $html_code = "";
	$html_code .= page_title();
	$html_code .= "<center><h2 class=\"text-primary\">Welcome!</h2></center>\n";
	@matches = find_matches();
	$html_code .= display_matches();
	return $html_code;
}

#writes the html code for when a user enters invalid username or passworld
#slight change to the sign in box to indicate the error. 
sub login_error{
	my $html_code = "";
	my $html_code .= page_title();

	open (F, "sign_in_error.txt") or die "cannot open navbar.txt";
	my @html_lines = <F>;
	foreach $line (@html_lines){
		$html_code = $html_code.$line;
	}
	close F;
	
	return $html_code;
}

sub finding_match{
	$sth = $dbh->sqlite_create_function( 'match', -1 , sub {return $compatibility }, 'create function' );
	$rv = $sth->execute() or die $DBI::errstr;
	if($rv < 0){
		print $DBI::errstr;
	}
}

#function that finds the matches for the user. To be displayed when the user logs in. 
#the gender preference will be retrieved from the preferences.txt from ther user database
#it will be then compared with the gender of each user, and then those who match will be 
#added to an array
sub find_matches{
	my $username = param('Username');
	my $html_code = "";
	my @matches = ();

	my $stmt = qq(SELECT gender from PREFERENCES WHERE username="$username";);
	$sth = $dbh->prepare( $stmt );	
	$rv = $sth->execute() or die $DBI::errstr;
	if($rv < 0){
		print $DBI::errstr;
	}

	@row = $sth->fetchrow_array();
	$pre_gender = $row[0];

	my @students = glob("$students_dir/*");
	foreach my $student (@students){
		$student =~ s/\.\/students\///ig;
	}

	foreach $student (@students){
		if ($student eq $username){
			next;
		}

		$stmt = qq(SELECT gender from USERS WHERE username="$student";);
		$sth = $dbh->prepare( $stmt );	
		$rv = $sth->execute() or die $DBI::errstr;
		if($rv < 0){
			print $DBI::errstr;
		}
		@row = $sth->fetchrow_array();
		if ($pre_gender eq $row[0]){
			push(@matches, $student);
		}
	}

	return @matches;

}

#function that takes in the set of gender matches for the user and displays it
#the format is similar to that of display_user and results
sub display_matches{
	my $html_code = "";
	my @display_matches = @matches;

	#writing the html code for each of the profiles in a panel
	$html_code .= "<div class=\"container\" align=\"middle\">\n";
	$html_code .= "<div class=\"row\">\n";

	foreach $student (@display_matches) {
		$stmt = qq(SELECT gender,birthdate, degree from USERS WHERE username="$student";);
		$sth = $dbh->prepare( $stmt );	
		$rv = $sth->execute() or die $DBI::errstr;
		if($rv < 0){
			print $DBI::errstr;
		}
	
		my @row = $sth->fetchrow_array();
	
		$html_code .= "<div class=\"panel panel-default\" style=\"width:700px\">\n";
		$html_code .= "  <div class=\"panel-heading\" align=\"left\">\n";
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
		$html_code .= "    <p class=\"text-primary\">Birthdate: $row[1] </p>\n";
		$html_code .= "    <p class=\"text-primary\">Degree: $row[2] </p>\n";
		$html_code .= "  </ul>\n";
		$html_code .= "  </div>\n";
		$html_code .= "</div>\n";
	
		$i += 1;
	}	
	$html_code .= "</div>\n";
	$html_code .= "</div>\n";

	return $html_code;

}

#function that displays all users. In one page it will display 10 users,
#parameter n is passed to keep track of the next user to display when scrolling through images. The user's info on gender, birthdate and degree are taken to be displayed
#parameter should equal to "browse" when this is called. 
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

	#writing the html code for each of the profiles in a panel
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
	
		$html_code .= "<div class=\"panel panel-default\" style=\"width:700px\">\n";
		$html_code .= "  <div class=\"panel-heading\" align=\"left\">\n";
		$html_code .= "	   <a href=\"love2041.cgi?state=profile&user=$students[$i]\"\n";
		$html_code .= "      <h3><b>$students[$i]</b></h3>\n";
		$html_code .= "    </a>\n";
		$html_code .= "  </div>\n";
		$html_code .= "  <div class=\"panel-body\">\n";
		$html_code .= "  <div style=\"float:left\">\n";
		$html_code .= "  <center><img src=\"./students/$students[$i]/profile.jpg\"></centre>\n";		
		$html_code .= "  </div>\n";
		$html_code .= "  <br><br>\n";
		$html_code .= "  <ul>\n";
		$html_code .= "    <p class=\"text-primary\">Gender: $row[0] </p>\n";
		$html_code .= "    <p class=\"text-primary\">Birthdate: $row[1] </p>\n";
		$html_code .= "    <p class=\"text-primary\">Degree: $row[2] </p>\n";
		$html_code .= "  </ul>\n";
		$html_code .= "  </div>\n";
		$html_code .= "</div>\n";
	
		$i += 1;
	}	
	$html_code .= "</div>\n";
	$html_code .= "</div>\n";

	$html_code .= "<div class=\"row\">\n";
	$html_code .= "<div class=\"container\" align=\"middle\">\n";

	#buttons for the next and prev
  	$html_code .= p(
 		start_form, "\n",
		hidden('n', $n-10),"\n",
		hidden('n'),"\n",
		hidden('user'),"\n",
		hidden('Prev'),"\n",
		hidden('Next'),"\n",
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

#html code for printing a single user's profile
#parameter n is used to keep track of the user to be displayed. Originally it was used to 
#toggle between the user profiles in subset 0
#with username given, the  function will print the image in a file before retreiving data
#from the database. After decoding the data, and string concat into two strings
#it will be placed in the html code
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

	#retrieving the information of a user, the field attributes are the same as the array
	#display_fields
	#below the fields of the user are placed into an array @row
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
	
	#concating all the info. Some information about users was not given, thus left out
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
        <h3 class=\"panel-title\">Personal Info</h3>
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
      <h3 class=\"panel-title\">Interests</h3>
  	</div>
    <div class=\"panel-body\">
	  <p class=\"text-info\">$interest</p>
	</div>
  	</div>
  	</div>
  </div>";

	return $html_code;

}

#page that will display the searched results. Function is used when state is in "search" mode
#client can enter a substring, consisting of alphabet and numbers. 
#the function will search through all the usernames that consist of that substring and push
#into an array. Usig the array, a list of usernames that match will be generated
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

#based on the number of items in @results, decide whether there are no results, one or many
	$html_code .= "<br><br>\n";
	$no_of_results = @results;
	if (!defined(@results)){
		$html_code .= "<center><h4 class=\"text-primary\">Sorry! There were no results found for <b>$search_string</b></h4></center>\n";
	} elsif ($no_of_results == 1) {
		$html_code .= "<center><h4 class=\"text-primary\"><b>$no_of_results</b>result found for <b>$search_string</b></h4></center><br><br>\n";
	} else {
		$html_code .= "<center><h4 class=\"text-primary\"><b>$no_of_results</b>result(s) found for <b>$search_string</b></h4></center><br><br>\n";
	}

#html code for displaying the results, the format is similar to the display in "browse" mode
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
			$html_code .= "  <div class=\"panel-heading\" align=\"left\">\n";
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
			$html_code .= "    <p class=\"text-primary\">Birthdate: $row[1] </p>\n";
			$html_code .= "    <p class=\"text-primary\">Degree: $row[2] </p>\n";
			$html_code .= "  </ul>\n";
			$html_code .= "  </div>\n";
			$html_code .= "</div>\n";
		}
		$html_code .= "</div>\n";
	}
	return $html_code;
}

#html code for sign in page
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

#from the information passed from the sign_in function, decide wheter the password is correct
sub authenticate{
	my $html_code = "";
	my $authenticated = 0;
	if (defined(param('state'))){
		if(param('state') ne "sign_in"){
			return;
		}
	}

	if(param('Username') && param('Password')){
		$username = param('Username');
		$password = param('Password');
		$html_code = hidden('Password');

		my $stmt = qq(SELECT password from USERS WHERE username="$username";);
		$sth = $dbh->prepare( $stmt );	
		$rv = $sth->execute() or die $DBI::errstr;
		if($rv < 0){
			print $DBI::errstr;
		}

		my @row = $sth->fetchrow_array();

		if (defined(@row)){
			if ($password eq $row[0]){
				$authenticated = 1;
			} else {
				$authenticated = 0;
			}
		} else {
			$authenticated = 0;
		}

	}
	return $authenticated;

}


#html code for the page navbar, this is before a user signs in. 
#right hand side has "register" and "sign in" buttons
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

#html code for the navbar when a user has logged in. the right handside of the navbar should
#only have "sign out" button which directs back to the homepage
sub page_navbar_login{

	open (F, "navbar_login.txt") or die "cannot open navbar.txt";
	my @html_lines = <F>;
	my $html_code = "";
	foreach $line (@html_lines){
		$html_code = $html_code.$line;
	}

	close F;
	return $html_code;
}

#title page for the website, which is shown below the navbar.
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

#function for returning header html code. Modifications were made from the source code
#added bootswatch source to for the formatting of the website
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
#below the function prints the end of the html code
#addition javascript stuff are added to enhance performance
sub page_trailer {
	my $html = "";
	$html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
	
	$html .= "<script src=\"http://code.jquery.com/jquery.min.js\"></script>\n";
	$html .= "<script src=\"js/bootstrap.min.js\"></script>\n";

	$html .= end_html;
	return $html;
}
