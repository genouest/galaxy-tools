use strict;
use warnings;
use Getopt::Long;

my $miranda;
my $mature;

GetOptions ("miranda=s" => \$miranda,
           	"mature=s"   => \$mature);


open MAT, $mature or die "failed to open $mature\n";
open OUT_MIR, ">mirna.asko.tsv" or die "failed to open mirna.asko.tsv";
my $mirna="";
my $mirna_seq="";
my $start=1;
print OUT_MIR "mirna\tseq\n";
while (<MAT>) {
  chomp;
  if (/^>(\S+)/) {
    unless ($start==1) {
      print OUT_MIR $mirna, "\t", $mirna_seq, "\n";
    }
    $start=0;
    $mirna=$1;
    $mirna_seq="";
    next;
  }
  $mirna_seq.=$_;
}
print OUT_MIR $mirna, "\t", $mirna_seq, "\n";


open MIRANDA, $miranda or die "failed to open $miranda\n";
open TARGET, ">target.asko.tsv" or die "failed to open target.asko.tsv\n";
print TARGET "target\ttargets\@mirna\ttargets\@mRNA\tscore\tenergy\talignment length\tglobal coverage\tseed coverage\n";

while (<MIRANDA>) {
  chomp;
  my ($mirna, $target, $score, $energy,$pos1, $pos2,$alnlength, $glcov, $seedcov)=split "\t";
  $mirna=~ s/^>//;
  $target=~s/_UTR3$//;
  $glcov=~ s/\%$//;
  $seedcov=~ s/\%$//;
  print TARGET join ("\t", $mirna.'.'.$target, $mirna, $target, $score, $energy,$alnlength, $glcov, $seedcov), "\n";
}
