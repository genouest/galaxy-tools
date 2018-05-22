#!/usr/bin/perl

=pod

GenoCopy

Created by Cyril MONJEAUD

=cut

use strict;
use warnings;
use File::Temp;
use File::Copy;
use File::Basename;
use YAML qw(LoadFile); ;

my @allowed_paths = ('/home/', '/omaha-beach/', '/groups/');

# ARGS
my ($src, $log_file, $dest_id, $work_dir, $merge)=@ARGV;
die("Absolute path required\n") unless $src =~ /^\//;
die("Paths containing '..' are disallowed\n") if $src =~ /\/\.\.\//;
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
                print MYLOGFILE "merge option is enable\n";
                print MYLOGFILE "folder : $src was found\nsub directories are ignored\nsearching files........\n\n";
                my $count_file_in_dir=0;

                # extract extension
                my $ext_fic='txt';
                opendir (DIR, $src) or die $!;
                while (my $file = readdir (DIR))
                        {

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
                open (MYFICFINAL, ">>".$work_dir."/primary_".$dest_id."_merge.file_visible_".$ext_fic);

                #for each file in this directory
                my $num_line_del=$ARGV[5];

                opendir (DIR, $src) or die $!;
                while (my $file = readdir (DIR))
                        {
                                # We only want files
                                next unless (-T "$src/$file");
                                next unless ("$src/$file"!~/\~$/);
                                $count_file_in_dir+=1;

                                # print in log_file
                                print MYLOGFILE "file : $src/$file was found\n";

                                # copy content file into final file
                                open (CURRENT_FILE, "$src/$file");
                                print MYLOGFILE "header : $num_line_del lines deleted\n\n";
                                my $num_line_current=0;
                                while (my $ligne = <CURRENT_FILE>)
                                        {
                                        $num_line_current+=1;
                                        next unless ($num_line_current > $num_line_del);
                                        print MYFICFINAL $ligne;
                                        }

                        }

                print MYLOGFILE "\nFiles are merged\n";

                #close directory and file
                closedir (DIR);
                close (MYFICFINAL);

                }
         else
                {
                 print MYLOGFILE "merge option is disable\n";
                 print MYLOGFILE "source : ".$src." is a directory\n";
                 opendir (DIR, $src) or die $!;
                 print MYLOGFILE "folder : $src was found\n\nsub directories are ignored\nsearching files........\n\n";
                 my $count_file_in_dir=0;

                 #for each file in this directory
                 while (my $file = readdir (DIR))
                        {
                                # We only want files
                                next unless (-f "$src/$file");
                                next unless ("$src/$file"!~/\~$/);

                                $count_file_in_dir+=1;

                                # extract name and extension
                                my ($base, $dir, $ext) = fileparse($file, qr/\.[^.]*/);
                                $ext=~s/\.//g;

                                # default extension
                                if ($ext eq '' or $ext eq ',')
                                        {$ext='txt';}

                                # replace all "_" by "."
                                $base=~s/_/./g;

                                # print in log_file
                                print MYLOGFILE "file : $src/$file is found. New name : $base.$ext\n";

                                # do a copy in tmp file directory
                                copy("$src/$file", $work_dir."/primary_".$dest_id."_".$base.".".$ext."_visible_".$ext) or print MYLOGFILE "Copy failed : Please check file permissions!\n" and $count_file_in_dir-=1;
                        }
                closedir (DIR);
                print MYLOGFILE "$count_file_in_dir files are copied\n\nplease REFRESH history if some files are missing\n";
                }
        }
else
  {
  # extract name and extension
  my ($base, $dir, $ext) = fileparse($src, '\..*');
  $ext=~s/\.//g;
  print MYLOGFILE "file : $src is found and copied\n\nplease REFRESH history if the the file is missing\n";

  # default extension
  if ($ext eq '' or $ext eq ',')
        {$ext='txt';}

  # replace all "_" by "."
  $base=~s/_/./g;
  copy($src, $work_dir."/primary_".$dest_id."_".$base."_visible_".$ext);
  }

close(MYLOGFILE);

exit;
__END__
