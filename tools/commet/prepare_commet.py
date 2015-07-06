import sys, os, re

"""

Created by Cyril Monjeaud
Cyril.Monjeaud@irisa.fr

"""

def __main__():

	# open the outpt file
	read_set=open(sys.argv[1], 'w')
        read_set.write("//commet input file//\n")

	# write the files path
	i = 2
	while i < len(sys.argv):
		read_set.write(sys.argv[i+1]+":")
                read_set.write(sys.argv[i].replace(",", ";")+"\n") 
		i = i+2 	

	# close output file
	read_set.close()

if __name__ == "__main__": __main__()
