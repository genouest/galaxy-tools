import subprocess, os, sys, shutil, tempfile, os.path
from os.path import basename, splitext

## inputs
kmer_value = sys.argv[7]
smallc_value = sys.argv[8]
bigc_value = sys.argv[9]
output_contex_value = sys.argv[10]
counts_value = sys.argv[11]
input_dat = sys.argv[12:len(sys.argv):2] # contains filename1... filenameq
input_ext = sys.argv[13:len(sys.argv):2] # contains extension1... extensionq

## tmp directory
tmp_dir = tempfile.mkdtemp(prefix='kissplice-galaxy.')

## command line (init)
command_line = []
command_line.append("kissplice")

## symlink for .fasta/q (extension required)
## command line built with -r option
identifier = ""
for i in range(0,len(input_dat)):
	tmp_input_fasta =  os.path.join(tmp_dir, 'input'+str(i)+'.'+input_ext[i])
	identifier += 'input'+str(i)+'_'
	os.symlink(input_dat[i], tmp_input_fasta)
	command_line.append("-r")
	command_line.append(tmp_input_fasta)

## command line (end)
opath=tmp_dir+"/results"
nocontext = ""
nosnp = ""
if output_contex_value == "yes":
	command_line.extend(["-k", kmer_value, 
			     "-c", smallc_value, "-C", bigc_value,
			     "--counts", counts_value, "--output-context",
			     "-o", opath, "-s"])
else:
	command_line.extend(["-k", kmer_value, 
			     "-c", smallc_value, "-C", bigc_value,
			     "--counts", counts_value,
			     "-o", opath, "-s"])

## running kissplice
p=subprocess.Popen(command_line, 
		   stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdoutput = p.communicate()

## outputs
output_f1=sys.argv[1]
out1=open(output_f1, 'w' )
out1.write(stdoutput[0])
out1.close()

output_type0=sys.argv[2]
output_type1=sys.argv[3]
output_type2=sys.argv[4]
output_type3=sys.argv[5]
output_type4=sys.argv[6]

result_type0 = opath+"/"+"results_"+identifier+"k"+kmer_value+"_coherents_type_0.fa"
result_type1 = opath+"/"+"results_"+identifier+"k"+kmer_value+"_coherents_type_1.fa"
result_type2 = opath+"/"+"results_"+identifier+"k"+kmer_value+"_coherents_type_2.fa"
result_type3 = opath+"/"+"results_"+identifier+"k"+kmer_value+"_coherents_type_3.fa"
result_type4 = opath+"/"+"results_"+identifier+"k"+kmer_value+"_coherents_type_4.fa"

shutil.move(result_type0, output_type0)
shutil.move(result_type1, output_type1)
shutil.move(result_type2, output_type2)
shutil.move(result_type3, output_type3)
shutil.move(result_type4, output_type4)

## cleaning
shutil.rmtree(tmp_dir)
