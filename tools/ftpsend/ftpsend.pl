#!/usr/bin/perl

use strict;
use warnings;
use File::Copy;
use File::Basename;

# SETTINGS
my $autocreate=1;

# VALIDATE INPUT
my ($ftp_dir, $subdir, $user, $logfile, @files)=@ARGV;
die("This galaxy instance does not have FTP enabled\n") unless $ftp_dir; # i.e. in universe_wsgi.ini
die("FTP dir, $ftp_dir, does not exist!\n") unless -d $ftp_dir;
die("Invalid email address: $user\n") if $user =~ /^[\.\/]/;
my $dest="$ftp_dir/$user/$subdir";
unless (-d $dest) {
    if ($autocreate) {
        mkdir($dest) or die("Unable to mkdir, $dest: $!\n");
        chmod 0775, $dest or die("Unable to chmod $dest: $!\n");
    } else {
        die("User $user does not have an FTP folder\n");
    }
}

# COPY FILES, WRITE TO LOG
open(OUT, ">$logfile") or die($!);
while (@files) {
    my $file=shift @files or die("Source filename required\n");
    my $name=shift @files or die("Destination filename required\n");
    die("Source file, $file, does not exist\n") unless -e $file;
    copy($file, "$dest/$name") or die($!);
    print OUT "The file $name is copied into your FTP server\n";
}
close OUT;
exit;
__END__
Copyright (c) 2011 US DOE Joint Genome Institute.
Use freely under the same license as Galaxy itself.
