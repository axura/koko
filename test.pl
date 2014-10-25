#!/usr/bin/perl -w 

#use strict
#testing perl file for all purposes. 

opendir $students_folder, 'students' or die "couldn't open folder students";

@folders = readdir $students_folder;


foreach my $user (@folders){
#	print "$folder\n";
	if ($user =~ /^[^a-z0-9].*$/ig){
#		print "$user\n";
		next;
	}
	$file_location = "students/".$user."/profile.txt";

	open(File, "$file_location") or die "cannot open the profile text for $user\n";
	@lines = <File>;
	$file_index = 0;
	foreach $line (@lines){
		$index = $file_index;
		if ($line =~ /^([a-z].*):/i){
			$field = $1;
			$index += 1;
			$entry = $lines[$index];
			chomp($entry);		
			print "$field $entry\n";
#			$password = $lines[$file_index+1];
#			chomp ($password);
#			$password =~ s/^\s*//ig;
		}
		chomp($line);
		$file_index += 1;
		
	}
	close(File);
}

closedir $students_folder;
