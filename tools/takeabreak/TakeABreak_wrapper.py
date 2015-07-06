import sys, tempfile, subprocess, glob
import os, re, shutil
import optparse
from os.path import basename

"""

Created by Cyril Monjeaud
Cyril.Monjeaud@irisa.fr

WARNING :

TakeABreak_wrapper.py needs:

- dbgh5 & TakeABreak binaries in your $PATH

All these files are available after compiling the sources of TakeABreak :

http://colibread.inria.fr/files/2014/01/TakeABreak-1.1.0-Source.tar_.gz

or with the package_takeabreak dependency in the toolshed

"""

def __main__():

	# create a special dir inside job working dir
        tmp_dir = tempfile.mkdtemp()
        os.chdir(tmp_dir)

        # retrieve arguments
        parser = optparse.OptionParser()
        parser.add_option("-i", dest="reads_files")
        parser.add_option("-k", dest="kmer")
        parser.add_option("-S", dest="kmersolid")

        parser.add_option("-g", dest="graph_file")
        parser.add_option("-c", dest="complexity")
        parser.add_option("-m", dest="maxsimprct")
        parser.add_option("-r", dest="optimization")

        parser.add_option("--output_graph")
        parser.add_option("--output_fasta")
        parser.add_option("--output_log")

        (options, args) = parser.parse_args()
	
	cmd_line=[]
	if options.reads_files:
		# start the command line
		cmd_line.append("TakeABreak")
		cmd_line.extend(["-in",options.reads_files,"-kmer-size",options.kmer,"-abundance",options.kmersolid])
	else:
		# start the command line
		os.symlink(options.graph_file, "graph.h5")
		cmd_line.append("TakeABreak")
		cmd_line.extend(["-graph", "graph.h5"])

	cmd_line.extend(["-out","galaxy","-lct",options.complexity,"-max-sim",options.maxsimprct,"-repeat",options.optimization])

	# execute command line 
	p=subprocess.Popen(cmd_line,
                   stdout=subprocess.PIPE,stderr=subprocess.PIPE)

	stdoutput, stderror = p.communicate()

        # log file
        logfile=open(options.output_log, "w")
	logfile.write("[COMMAND LINE]"+' '.join(cmd_line)+"\n\n")
        logfile.write(stdoutput)
	logfile.write(stderror)
	logfile.close()
	
	if options.reads_files:

                # create output h5
		shutil.copy("galaxy.h5", options.output_graph)

        # create output fasta
	shutil.copy("galaxy.fasta", options.output_fasta)

if __name__ == "__main__": __main__()

