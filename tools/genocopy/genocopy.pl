#!/usr/bin/perl

=pod

GenoCopy

Created by Cyril MONJEAUD

=cut

use strict;
use warnings;
use File::Temp;
use File::Copy;
use File::Copy::Recursive qw(dircopy);
use File::Basename;
use File::Spec;
use YAML qw(LoadFile); ;

my @allowed_paths = ('/home/', '/omaha-beach/', '/groups/', '/bipaa-data/', '/scratch');

# ARGS
my ($src, $log_file, $work_dir, $merge)=@ARGV;
die("Absolute path required\n") unless $src =~ /^\//;
die("Paths containing '..' are disallowed\n") if $src =~ /\/\.\.\//;

# Make sure the path is absolute
$src = File::Spec->rel2abs($src);

my $ok=0;
foreach my $dir (@allowed_paths) {
    my $re="^$dir";
    $re =~ s/\//\\\//g;
    if ($src =~ /$re/) {
        $ok=1;
        last;
    }
}
die("Not an allowed source path\n") unless $ok;
die("File or directory not found\n") unless -d $src or -e $src;

#open log file
open (MYLOGFILE, '>>'.$log_file);

#if directory or not
if (-d $src)
    {
     $src=~s/\/$//g;
     if ($merge eq 'true')
        {
        print MYLOGFILE "Merging files in directory\n";
        print MYLOGFILE "Folder: $src was found\nsub directories are ignored in merging mode\nsearching files........\n\n";
        my $count_file_in_dir=0;

        # Guess extension
        my $ext_fic='txt';
        opendir (DIR, $src) or die $!;
        while (my $file = readdir (DIR)) {
            # Next if extension is already found
            next unless ($ext_fic eq 'txt' or $ext_fic eq '');

            # We don't want binary or cached files
            next unless (-T "$src/$file");
            next unless ("$src/$file"!~/\~$/);

            # extract extension
            my ($base, $dir, $ext) = fileparse($file, qr/\.[^.]*/);
            $ext=~s/\.//g;
            $ext_fic = $ext;
        }
        closedir(DIR);

        # create and open final file
        open (MYFICFINAL, ">>".$work_dir."/merged.".$ext_fic);

        #for each file in this directory
        my $num_line_del=$ARGV[4];

        opendir (DIR, $src) or die $!;
        while (my $file = readdir(DIR)) {
            # We only want files
            next unless (-T "$src/$file");
            next unless ("$src/$file"!~/\~$/);
            $count_file_in_dir+=1;

            # print in log_file
            print MYLOGFILE "file: $src/$file was found\n";

            # copy content file into final file
            open (CURRENT_FILE, "$src/$file");
            print MYLOGFILE "header: $num_line_del lines deleted\n\n";
            my $num_line_current=0;
            while (my $ligne = <CURRENT_FILE>)
                {
                $num_line_current+=1;
                next unless ($num_line_current > $num_line_del);
                print MYFICFINAL $ligne;
                }
        }

        print MYLOGFILE "\nFiles were merged\n";

        #close directory and file
        closedir (DIR);
        close (MYFICFINAL);
        }
     else
        {
         print MYLOGFILE "Not merging anything\n";
         print MYLOGFILE "Directory $src was copied\n";

         dircopy($src, $work_dir)
        }
    }
else {
  # Just a file
  # extract name and extension
  my ($base, $dir, $ext) = fileparse($src, '\..*');
  $ext=~s/\.//g;
  print MYLOGFILE "File: $src was copied\n";

  # default extension
  if ($ext eq '' or $ext eq ',')
    {$ext='txt';}

  # replace all "_" by "."
  $base=~s/_/./g;
  copy($src, $work_dir."/".$base.".".$ext);
}

print MYLOGFILE "\nYou might need to refresh your history to see the copied dataset.\n";

close(MYLOGFILE);

exit;
__END__
