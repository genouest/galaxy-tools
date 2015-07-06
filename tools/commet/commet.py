#!/usr/bin/env python
import sys, tempfile, subprocess, glob
import os, re, shutil, optparse
import zipfile, tarfile, gzip
from os.path import basename

"""
WARNING :

commet.py needs commet_exe binaries in your $PATH

commet is available after compiling sources :

http://github.com/pierrepeterlongo/commet

or with the galaxy_commet package in the GenOuest toolshed (coming soon)

NOTE : 

please add the line #!/usr/bin/env python in top of the Commet.py file if you've a bash error.


"""

def __main__():

	# arguments recuperation
        parser = optparse.OptionParser()
        parser.add_option("--input", dest="input")
        parser.add_option("-k", dest="kmer")
        parser.add_option("-t", dest="minsharedkmer")
        parser.add_option("-l", dest="minlengthread")
        parser.add_option("-n", dest="maxn")
        parser.add_option("-e", dest="minshannonindex")
        parser.add_option("-m", dest="maxreads")

        parser.add_option("--output")
        parser.add_option("--output_vectors")
        parser.add_option("--output_dendro")
        parser.add_option("--output_logs")
        parser.add_option("--output_matrix")
        parser.add_option("--output_heatmap1")
        parser.add_option("--output_heatmap2")
        parser.add_option("--output_heatmap3")

        (options, args) = parser.parse_args()


	# copy R script into the current dir
	shutil.copy(os.environ['RSCRIPTS']+"/heatmap.r", os.getcwd())
        shutil.copy(os.environ['RSCRIPTS']+"/dendro.R", os.getcwd())

	# remove the first line of the input file
	commet_file = open(options.input, "r")
	commet_file_clean = open("commet_clean_file", "w")

	# delete the first line
	commet_file.readline()
	for line in commet_file:
		commet_file_clean.write(line)

	# close files
	commet_file.close()
	commet_file_clean.close()

	# edit the command line
	cmd_line=[]
	cmd_line.append("Commet.py")
	cmd_line.extend(["commet_clean_file","-b",os.environ['BINARIES'],"-k",options.kmer,"-t",options.minsharedkmer,"-l",options.minlengthread,"-e",options.minshannonindex])

	# add options
	if options.maxn:
		
		#cmd_line += ' -n '+options.maxn+' -m '+options.maxreads+' > '+options.output+' 2>>'+options.output
		cmd_line.extend(["-n",options.maxn,"-m",options.maxreads])
	#else:
		#cmd_line += ' > '+options.output+' 2>>'+options.output

	# execute job
	p=subprocess.Popen(cmd_line,
                   stdout=subprocess.PIPE,stderr=subprocess.PIPE)

	stdoutput, stderror = p.communicate()

	# log file
        logfile=open(options.output, "w")
	logfile.write("[COMMAND LINE]"+' '.join(cmd_line)+"\n\n")
	logfile.write(str(stdoutput))
	logfile.write(str(stderror))
	logfile.close()

	# copy .bv files inside a .bv archive
	tmp_output_dir=os.getcwd()+"/output_commet/"
        os.chdir(tmp_output_dir)

	# create zip outputs
        mybvzipfile=zipfile.ZipFile(tmp_output_dir+'bv.zip.temp', 'w')
        mylogzipfile=zipfile.ZipFile(tmp_output_dir+'log.zip.temp', 'w')
        mymatrixzipfile=zipfile.ZipFile(tmp_output_dir+'matrix.zip.temp', 'w')

	# write files into the specific archive
        list_files = glob.glob(tmp_output_dir+'/*')
        for i in list_files:

		if re.search("\.bv$", i):
			mybvzipfile.write(os.path.basename(i))
		if re.search("\.log$", i):
                        mylogzipfile.write(os.path.basename(i))
		if re.search(".csv$", i):
                        mymatrixzipfile.write(os.path.basename(i))

	# close zip files
	mybvzipfile.close()
	mylogzipfile.close()
        mymatrixzipfile.close()

	# return the archives
	shutil.move(tmp_output_dir+'bv.zip.temp', options.output_vectors)
	shutil.move(tmp_output_dir+'log.zip.temp', options.output_logs)
        shutil.move(tmp_output_dir+'matrix.zip.temp', options.output_matrix)

	# outputs
        shutil.move(tmp_output_dir+'dendrogram_normalized.png', options.output_dendro)
	shutil.move(tmp_output_dir+'heatmap_normalized.png', options.output_heatmap1)
	shutil.move(tmp_output_dir+'heatmap_percentage.png', options.output_heatmap2)
	shutil.move(tmp_output_dir+'heatmap_plain.png', options.output_heatmap3)

if __name__ == "__main__": __main__()

