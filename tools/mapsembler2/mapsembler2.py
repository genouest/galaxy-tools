#!/usr/bin/env python
import sys, subprocess, glob
import os, re, shutil, optparse
from os.path import basename

"""
WARNING :

Mapsembler2.py needs mapsembler2_exe binaries in your $PATH

Mapsember2 is available after compiling sources :

http://www.irisa.fr/symbiose/people/ppeterlongo/mapsembler2_2.2.3.zip

or with the galaxy_mapsembler2 package in the GenOuest toolshed


"""

def __main__():

	# arguments recuperation
        parser = optparse.OptionParser()
        parser.add_option("-s", dest="input_starters")
        parser.add_option("-r", dest="input_files")
        parser.add_option("-t", dest="output_extension")
        parser.add_option("-k", dest="kmer")
        parser.add_option("-c", dest="coverage")
        parser.add_option("-d", dest="substitutions")
        parser.add_option("-g", dest="genome_size")
        parser.add_option("-f", dest="process_search")
        parser.add_option("-x", dest="max_length")
        parser.add_option("-y", dest="max_depth")
        parser.add_option("--output")
        parser.add_option("-i", dest="index_files")

        (options, args) = parser.parse_args()

	# import tools
	os.symlink(os.environ['TOOLS'], os.getcwd()+'/tools')

	# execute mapsembler
	cmd_line=[]
	cmd_line.append("run_mapsembler2_pipeline.sh")

	# change starter extension
	cmd_line.extend(["-s", options.input_starters])

	#inputs
	cmd_line.append("-r")

	#cmd_line.append(inputs)
	cmd_line.append(' '.join(options.input_files.split(",")))

	# add parameters into the command line
	cmd_line.extend(["-t", options.output_extension, "-k", options.kmer, "-c", options.coverage, "-d", options.substitutions, "-g", options.genome_size, "-f", options.process_search, "-x", options.max_length, "-y", options.max_depth])
	
	# open the output log file
        log = open(options.output, "w")
	log.write("[COMMAND LINE] "+' '.join(cmd_line))

	process=subprocess.Popen(cmd_line,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdoutput, stderror = process.communicate()
	
	# results recuperation
	log.write(stdoutput)
	log.write(stderror)

	# close log file
	log.close()
	
	# move results files inside the job_outputs dir
	os.mkdir("job_outputs")
	result_files = glob.glob("res_*")
	for file in result_files:
		shutil.move(file, "job_outputs/")


	# move index files
	if options.index_files == "true":
	        index_files = glob.glob("index_*")
		for index in index_files:
			shutil.move(index, "job_outputs/")

	# move json result into gjson
        json_files = glob.glob("job_outputs/*.json")
        for json in json_files:
		shutil.move(json, json.replace(".json", ".gjson"))


if __name__ == "__main__": __main__()

