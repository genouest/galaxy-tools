#!/usr/bin/perl

=pod
GenoLink

usage:

genolink.pl  source  dest

Created by Cyril MONJEAUD
=cut

use strict;
use File::Copy;
use File::Basename;

# allowed path
my @allowed_paths = ('/home/', '/omaha-beach/', '/groups/', '/db/');

# arguments recuperation
my ($src, $dest, $symlink)=@ARGV;
die("Absolute path required\n") unless $src =~ /^\//;
die("Paths containing '..' are disallowed\n") if $src =~ /\/\.\.\//;

# allowed path transformation
my $ok=0;
foreach my $dir (@allowed_paths) {
    my $re="^$dir";
    $re =~ s/\//\\\//g;
    if ($src =~ /$re/) {
        $ok=1;
        last;
    }
}

# extract and print file name
my $basename = basename($src);
print "ORIGINAL NAME : ".$basename;


die("Not an allowed source path\n") unless $ok;
die("Path is not a file or is not accessible") unless -f $src;
die("File not found\n") unless -e $src;

# create the symbolic link
unlink($dest);
symlink($src, $dest);

exit;
__END__
