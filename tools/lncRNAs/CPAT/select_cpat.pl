my $cpat= shift;
my $score = shift;

open CPAT, $cpat or die "failed to open $cpat\n";
my $entete=<CPAT>;
while (<CPAT>) {
	my @F = split;
	if ($F[5] < $score) {print $F[0], "\n"} 
}
