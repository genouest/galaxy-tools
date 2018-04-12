use strict;
use warnings;

my $miranda=shift;
open MIRANDA, $miranda or die "failed to open $miranda\n";

print "mirna\ttargets\@mRNA\tscore\tenergy\talignment length\tglobal coverage\tseed coverage\n";

while (<MIRANDA>) {
  chomp;
  my ($mirna, $target, $score, $energy,$pos1, $pos2,$alnlength, $glcov, $seedcov)=split "\t";
  $mirna=~ s/^>//;
  $target=~s/_UTR3$//;
  $glcov=~ s/\%$//;
  $seedcov=~ s/\%$//;
  print join ("\t", $mirna, $target, $score, $energy,$alnlength, $glcov, $seedcov), "\n";
}
