#!/usr/bin/perl

=pod

GenoSend

Created by Cyril MONJEAUD

=cut

use strict;
use File::Copy;
use File::Basename;
use YAML qw(LoadFile); ;

use File::Basename;
my $dirname = dirname(__FILE__);

# ARGS
my ($email, $dest, $logfile, @files)=@ARGV;
die("Absolute path required\n") unless $dest =~ /^\//;
die("Paths containing '..' are disallowed\n") if $dest =~ /\/\.\.\//;

# Make sure the path is absolute
$dest = File::Spec->rel2abs($dest);

die("Only /home/*, /groups/* and /omaha-beach/* paths are allowed\n") unless $dest =~ /^\/home\// or $dest =~ /^\/groups\// or $dest =~ /^\/omaha-beach\// or $dest =~ /^\/scratch\//;
die("Destination folder does not exist: $dest\n") unless -e $dest;
die("Destination path is not a folder: $dest\n") unless -d $dest;


# CP
open(OUT, ">$logfile") or die($!);
my $nb_file_copied=0;
while (@files) {
    my $file=shift @files or die("Source filename required\n");
    my $name=shift @files or die("Destination filename required\n");
    print OUT "$file is copied, the new file is $dest/$name\n";
    copy($file, "$dest/$name") or die("Copy error : check that the Galaxy user has write access to the destination directory or that it exists");
    `bash -lc "/usr/bin/sudo -S $dirname/chown_genosend.sh '$dest/$name' '$email'"`;
    $nb_file_copied+=1;

}
close OUT;
print "Exported ", $nb_file_copied, " files into $dest\n";
exit;
__END__
Copyright (c) 2011 US DOE Joint Genome Institute.
Use freely under the same license as Galaxy itself.
