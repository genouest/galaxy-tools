import sys, tempfile, subprocess, glob
import os, re, shutil, stat
import optparse
from os.path import basename

"""

Created by Cyril Monjeaud
Cyril.Monjeaud@irisa.fr
Modified by Fabrice Legeai
fabrice.legeai@rennes.inra.fr

Last modifications : 04/21/2015

WARNING :

discoSNP++.py needs:

- run_discoSnp++.sh
- discoSNP++_to_genotypes.py
- the build repository next to the scripts

All these files are available after compiling the sources of discoSNP :

https://colibread.inria.fr/files/2013/10/DiscoSNPpp-2.0.6-Source.zip

or with the package_discoSnp_plus_plus package in the toolshed

"""


def __main__():

	# store inputs in an array
	parser = optparse.OptionParser()
	parser.add_option("-r", dest="data_files")
	parser.add_option("-b", dest="branching_bubbles")
	parser.add_option("-D", dest="deletions")
	parser.add_option("-P", dest="min_snps")
	parser.add_option("-l", action="store_true", dest="low_complexity")
	parser.add_option("-k", dest="kmer")
	parser.add_option("-t", action="store_true", dest="left_right_unitigs")
	parser.add_option("-T", action="store_true", dest="left_right_contigs")
	parser.add_option("-c", dest="coverage")
        parser.add_option("-C", dest="maxcoverage")
	parser.add_option("-d", dest="error_threshold")
	parser.add_option("-n", action="store_true", dest="genotypes")
	parser.add_option("-G", dest="reference")
        parser.add_option("-M", dest="mapping_error")

	(options, args) = parser.parse_args()

        # create the working dir inside job_working_dir
        output_dir = os.mkdir("job_outputs")

	cmd_line=[]
	cmd_line.append("/bin/bash")
	#cmd_line.append("/home/genouest/inrarennes/flegeai/local/DiscoSNP/DiscoSNP++-2.1.4-Source/run_discoSnp++.sh")
	cmd_line.append("run_discoSnp++.sh")
	#cmd_line.append("-B /local/bwa/bwa-0.7.10/")

	# transform .dat into .fasta or .fastq for kissreads2
	link_files=[]
	f = open(options.data_files, 'r')
	files = f.readlines()
	for file in files:
		file=file.strip()
		if re.search("^$",file): continue
		tagfile=[]
		tagfile=re.split('::', file)	
		number = int(tagfile[0])+1
		if re.search("^>.*", open(tagfile[1]).readline()):
                        link_file = 'input'+str(number)+'.fasta'
                else:
                        link_file = 'input'+str(number)+'.fastq'

                os.symlink(tagfile[1], link_file)
                link_files.append(link_file)


	# edit the command line
	cmd_line.extend(["-r",' '.join(link_files),"-b",options.branching_bubbles,"-D",options.deletions,"-P",options.min_snps,"-k",options.kmer,"-c",options.coverage,"-C",options.maxcoverage,"-d",options.error_threshold])
	if options.low_complexity:
		cmd_line.append("-l")
	if options.left_right_unitigs:
		cmd_line.append("-t")
	if options.left_right_contigs:
                cmd_line.append("-T")
	if options.genotypes:
		cmd_line.append("-n")

	# genotype part
	if options.reference:
		cmd_line.extend(["-G", options.reference])
		cmd_line.extend(["-M", options.mapping_error])

	cmd_line.extend(["-p","job_outputs/galaxy"])

	# execute job
	p=subprocess.Popen(cmd_line,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	stdoutput, stderror = p.communicate()

	# report file
        logfile=open("report.txt", "w")
	logfile.write("[COMMAND LINE]"+' '.join(cmd_line)+"\n\n")
	logfile.write(stdoutput)

	# print stderror because it's informations
        logfile.write(stderror)

	# close logfile
	logfile.close()

	# change .fa extension to .fasta for a correct print inside Galaxy
        fafiles = glob.glob("job_outputs/*_coherent.fa")
	for fafile in fafiles:
        	shutil.move(fafile, "coherent.fasta")
        vcffiles = glob.glob("job_outputs/*_coherent.vcf")
	for vcffile in vcffiles:
        	shutil.move(vcffile, "coherent.vcf")


if __name__ == "__main__": __main__()

