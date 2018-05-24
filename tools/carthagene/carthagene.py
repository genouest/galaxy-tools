#!/usr/bin/env python
import sys, tempfile, subprocess, glob
import os
import shutil
from os.path import basename


def __main__():

	# retrieve arguments
        input_script = sys.argv[1]
        output_file = sys.argv[2]
	output_id = sys.argv[3]
	dir = sys.argv[4]

	#print sys.argv
	#print "new file path : "+dir

	# create the working dir
	tmp_dir = tempfile.mkdtemp(dir=os.environ['GALAXY_HOME']+'/database/tmp/')
	os.chdir(tmp_dir)

	# copy input script
	cmd = 'ln -s '+input_script+' script'
	proc = subprocess.Popen( args=cmd, shell=True )
        returncode = proc.wait()

	#print "args length : "+str(len(sys.argv))

	# in case of data associated with the script
	i = 5
	data_tab = []
	while i < len(sys.argv):
		data_tab.append(sys.argv[i+1])
		cmd = 'ln -s '+sys.argv[i]+' '+sys.argv[i+1]
		#print "cmd = "+cmd
	        proc = subprocess.Popen( args=cmd, shell=True )
        	returncode = proc.wait()
		i = i+2

	# execute carthagene in the tmp_dir

	cmd = 'cat script | carthagene >'+output_file+' 2>&1'
	proc = subprocess.Popen( args=cmd, shell=True )
        returncode = proc.wait()

	# copy the outputs in the __new_file_path__
	cmd = 'rm script'
        proc = subprocess.Popen( args=cmd, shell=True )
        returncode = proc.wait()

	for file in data_tab:
	        cmd = 'rm '+file
        	proc = subprocess.Popen( args=cmd, shell=True )
	        returncode = proc.wait()

	list_files = glob.glob('*')
	for i in list_files:
		file_ext=(os.path.splitext(i)[1]).split('.')[-1]
		file_name=os.path.basename(os.path.splitext(i)[0])
		file_name=file_name.replace("_", "-")
        	command='cp '+i+' '+dir+'/primary_'+output_id+'_'+file_name+'_visible_'+file_ext
		proc = subprocess.Popen( args=command, shell=True )
		returncode = proc.wait()

        # remove the temp dir
        #os.chdir(os.environ['GALAXY_HOME']+'/database/tmp')
        #cmd = 'rm -rf '+tmp_dir
        #proc = subprocess.Popen( args=cmd, shell=True )
        #returncode = proc.wait()
	shutil.rmtree( tmp_dir )

if __name__ == "__main__": __main__()
