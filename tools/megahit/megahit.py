#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import shutil
import subprocess
import argparse

"""

Created by Cyril Monjeaud
Cyril.Monjeaud@irisa.fr

Last modifications : 07/06/2015

megahit.py needs:

	- megahit binaries

Binaries are available after compiling the sources :

https://github.com/voutcn/megahit

or with the package_megahit_0_3_2 repository in the toolshed

"""

def __main__():

    # arguments recuperation
    parser = argparse.ArgumentParser()
    parser.add_argument('-1', dest='paired1', nargs='+')
    parser.add_argument('-2', dest='paired2', nargs='+')
    parser.add_argument('-12', dest="interleaved", nargs='+')
    parser.add_argument('-r', dest="single", nargs='+')

    parser.add_argument('--min-contig-len', dest='mincontiglen')

    #basic assembly
    parser.add_argument('--min-count', dest='mincount')
    parser.add_argument('--k-min', dest='kmin')
    parser.add_argument('--k-max', dest='kmax')
    parser.add_argument('--k-step', dest='kstep')

    #advanced assembly
    parser.add_argument('--no-mercy', dest='nomercy')
    parser.add_argument('--no-bubble', dest='nobubble')
    parser.add_argument('--merge-level', dest='mergelevel')
    parser.add_argument('--prune-level', dest='prunelevel')
    parser.add_argument('--low-local-ratio', dest='lowlocalratio')
    parser.add_argument('--no-local', dest='nolocal')
    parser.add_argument('--kmin-1pass', dest='kmin1pass')

    parser.add_argument('--log', dest="log")
    parser.add_argument('--fasta', dest="fasta")

    args = parser.parse_args()

    # command line construction
    cmd_line = ['megahit']
    if args.paired1:
        cmd_line.extend(['-1', ','.join(args.paired1)])
        cmd_line.extend(['-2', ','.join(args.paired2)])
    elif args.interleaved:
        cmd_line.extend(['-12', ','.join(args.interleaved)])
    else:
        cmd_line.extend(['-r', ','.join(args.single)])

    cmd_line.extend(['--min-contig-len', args.mincontiglen])

    # command line basic options
    cmd_line.extend(['--min-count', args.mincount, '--k-min', args.kmin, '--k-max', args.kmax, '--k-step', args.kstep])

    # command line advanced options 
    if args.nomercy == "true":
	cmd_line.append('--no-mercy')
    if args.nobubble == "true":
        cmd_line.append('--no-bubble')
    if args.nolocal == "true":
        cmd_line.append('--no-local')
    if args.kmin1pass == "true":
        cmd_line.append('--kmin-1pass')

    cmd_line.extend(['--merge-level', args.mergelevel, '--prune-level', args.prunelevel, '--low-local-ratio', args.lowlocalratio])

    print "[CMD_LINE] "+' '.join(cmd_line)+"\n"

    # command with dependencies installed
    p = subprocess.Popen(cmd_line)
    p.communicate()

    try:
        shutil.copy("megahit_out/final.contigs.fa", args.fasta)
        shutil.copy("megahit_out/log", args.log)
    except:
        print "Output files are not generate. Please read the stderr"
        sys.exit(1)

if __name__ == '__main__':
    __main__()


			
