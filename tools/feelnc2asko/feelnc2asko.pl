use strict;
use warnings;
use Getopt::Long;
use Bio::Tools::GFF;

my ($anngff, $lncgff, $newgff);

GetOptions("ann=s" => \$anngff, "lnc=s" => \$lncgff, "new=s" => \$newgff);

my $gffout = Bio::Tools::GFF->new(-fh=> \*STDOUT, -gff_version => 3);

#1. the standard annotation
my $gffin = Bio::Tools::GFF->new(-file => $anngff, -gff_version => 3);


while (my $feature = $gffin->next_feature()) {
	if ($feature-> primary_tag eq 'mRNA') {
    my ($gene)=$feature->get_tag_values("gene");
    $feature->remove_tag("Parent");
    $feature->add_tag_value("Parent", $gene);
    $feature->add_tag_value("feelnc_type", "standard");
    $gffout->write_feature($feature);
  }
  if ($feature-> primary_tag eq 'gene') {
    my ($name)=$feature->get_tag_values("Name");
    $feature->remove_tag("ID");
    $feature->add_tag_value("ID", $name);
    $feature->add_tag_value("feelnc_type", "standard");
    $gffout->write_feature($feature);
  }
}
$gffin->close();


my %genes=();
my %transcripts=();

#2. The lncRNA gtf
my $fncgtf = Bio::Tools::GFF->new( -file => $lncgff, -gff_version => '2' );

while (my $feat = $fncgtf->next_feature()) {
	next if ($feat->primary_tag() ne 'exon');

	my $mrna= ($feat->get_tag_values('transcript_id'))[0];
  my $gene= ($feat->get_tag_values('gene_id'))[0];
#	print STDERR "str: ", $feat->strand(), "\n";
	if (exists($genes{$gene})) {
		if ($genes{$gene}->start() > $feat->start()) {
        	$genes{$gene}->start($feat->start());
        }
        if ($genes{$gene}->end() < $feat->end()) {
        	$genes{$gene}->end($feat->end());
        }
	}
  else {
    my $geneft = Bio::SeqFeature::Generic->new(
			-start       => $feat->start(),
			-end         => $feat->end(),
			-strand      => $feat->strand(),
			-primary_tag => 'gene',
			-source_tag  => $feat->source_tag(),
			-seq_id => $feat->seq_id());
#    $geneft->add_tag_value("feelnc_type", "lncRNA");
		$genes{$gene}=$geneft;
    $geneft->add_tag_value("ID", $gene);
}

if (exists($transcripts{$mrna})) {
		if ($transcripts{$mrna}->start() > $feat->start()) {
        	$transcripts{$mrna}->start($feat->start());
        }
        if ($transcripts{$mrna}->end() < $feat->end()) {
        	$transcripts{$mrna}->end($feat->end());
        }
  }
	else {
		my $tr = Bio::SeqFeature::Generic->new(
			-start       => $feat->start(),
			-end         => $feat->end(),
			-strand      => $feat->strand(),
			-primary_tag => 'mRNA',
			-source_tag  => $feat->source_tag(),
			-seq_id => $feat->seq_id());
		$tr->add_tag_value("ID", $mrna);
    $tr->add_tag_value("Parent",$gene);
    $tr->add_tag_value("feelnc_type", "lncRNA");
		$transcripts{$mrna}=$tr;
	}
}

#3. The new mRNA gtf
my $nmgtf = Bio::Tools::GFF->new( -file => $newgff, -gff_version => '2' );

while (my $feat = $nmgtf->next_feature()) {
	next if ($feat->primary_tag() ne 'exon');

	my $mrna= ($feat->get_tag_values('transcript_id'))[0];
  my $gene= ($feat->get_tag_values('gene_id'))[0];
#	print STDERR "str: ", $feat->strand() , "\n";
	if (exists($genes{$gene})) {
		if ($genes{$gene}->start() > $feat->start()) {
        	$genes{$gene}->start($feat->start());
        }
        if ($genes{$gene}->end() < $feat->end()) {
        	$genes{$gene}->end($feat->end());
        }
	}
  else {
    my $geneft = Bio::SeqFeature::Generic->new(
			-start       => $feat->start(),
			-end         => $feat->end(),
			-strand      => $feat->strand(),
			-primary_tag => 'gene',
			-source_tag  => $feat->source_tag(),
			-seq_id => $feat->seq_id());
		$geneft->add_tag_value("ID", $gene);
#    $geneft->add_tag_value("feelnc_type", "new");
		$genes{$gene}=$geneft;
}

if (exists($transcripts{$mrna})) {
		if ($transcripts{$mrna}->start() > $feat->start()) {
        	$transcripts{$mrna}->start($feat->start());
        }
        if ($transcripts{$mrna}->end() < $feat->end()) {
        	$transcripts{$mrna}->end($feat->end());
        }
  }
	else {
		my $tr = Bio::SeqFeature::Generic->new(
			-start       => $feat->start(),
			-end         => $feat->end(),
			-strand      => $feat->strand(),
			-primary_tag => 'mRNA',
			-source_tag  => $feat->source_tag(),
			-seq_id => $feat->seq_id());
		$tr->add_tag_value("ID", $mrna);
    $tr->add_tag_value("Parent",$gene);
    $tr->add_tag_value("feelnc_type", "new");
		$transcripts{$mrna}=$tr;
	}
}

foreach my $mrna (keys %transcripts) {
	my ($parent)=$transcripts{$mrna}->get_tag_values("Parent");
  $gffout->write_feature($genes{$parent});
  $gffout->write_feature($transcripts{$mrna});
}
