#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import os
import tempfile
import shutil
import subprocess
import glob
import argparse
from os.path import basename
import zipfile
import tarfile
import gzip
from galaxy.datatypes.checkers import *
from stacks import *


def __main__():

    # arguments recuperation

    parser = argparse.ArgumentParser()
    parser.add_argument('-P')
    parser.add_argument('-M')
    parser.add_argument('-b')
    parser.add_argument('--vcf')
    parser.add_argument('--genepop')
    parser.add_argument('--structure')
    parser.add_argument('-e')
    parser.add_argument('--genomic')
    parser.add_argument('--fasta')
    parser.add_argument('--phase')
    parser.add_argument('--beagle')
    parser.add_argument('--plink')
    parser.add_argument('--phylip')
    parser.add_argument('--phylip_var')
    parser.add_argument('--write_single_snp')
    parser.add_argument('-k')

    # advanced options

    parser.add_argument('-B')
    parser.add_argument('-W')
    parser.add_argument('-r')
    parser.add_argument('-p')
    parser.add_argument('-m')
    parser.add_argument('-a')
    parser.add_argument('-f')
    parser.add_argument('--p_value_cutoff')
    parser.add_argument('--window_size')
    parser.add_argument('--bootstrap')
    parser.add_argument('--bootstrap_reps')

    # multifile management

    parser.add_argument('--logfile')

    # outputs

    parser.add_argument('--ss')
    parser.add_argument('--s')

    # optional outputs

    parser.add_argument('--ov')
    parser.add_argument('--op')
    parser.add_argument('--ol')
    parser.add_argument('--of')
    parser.add_argument('--os')
    parser.add_argument('--oe')
    parser.add_argument('--om')
    parser.add_argument('--og')
    parser.add_argument('--unphased_output')
    parser.add_argument('--markers_output')
    parser.add_argument('--phase_output')
    parser.add_argument('--fst_output')

    options = parser.parse_args()

    # create the working dir
    os.mkdir('job_outputs')
    os.mkdir('galaxy_outputs')

    os.chdir('job_outputs')

    # STACKS_archive
    # check if zipped files are into the tab
    extract_compress_files(options.P, os.getcwd())

    # create the populations command input line
    cmd_files = ' -b ' + options.b + ' -P ' + os.getcwd() + ' '

    # create the populations command line
    cmd_options = ''

    if options.e:
        cmd_options += ' -e ' + options.e
    if options.M:
        cmd_options += ' -M ' + options.M
    if options.vcf and options.vcf == 'true':
        cmd_options += ' --vcf '
    if options.genepop and options.genepop == 'true':
        cmd_options += ' --genepop '
    if options.structure and options.structure == 'true':
        cmd_options += ' --structure '
    if options.genomic and options.genomic == 'true':
        cmd_options += ' --genomic '
    if options.fasta and options.fasta == 'true':
        cmd_options += ' --fasta '
    if options.phase and options.phase == 'true':
        cmd_options += ' --phase '
    if options.beagle and options.beagle == 'true':
        cmd_options += ' --beagle '
    if options.plink and options.plink == 'true':
        cmd_options += ' --plink '
    if options.phylip and options.phylip == 'true':
        cmd_options += ' --phylip '
    if options.phylip_var and options.phylip_var == 'true':
        cmd_options += ' --phylip_var '
    if options.write_single_snp and options.write_single_snp == 'true':
        cmd_options += ' --write_single_snp '
    if options.k and options.k == 'true':
        cmd_options += ' -k '
    if options.B:
        cmd_options += ' -B ' + options.B
    if options.W:
        cmd_options += ' -W ' + options.W
    if options.r:
        cmd_options += ' -r ' + options.r
    if options.p:
        cmd_options += ' -p ' + options.p
    if options.m:
        cmd_options += ' -m ' + options.m
    if options.a:
        cmd_options += ' -a ' + options.a
    if options.f:
        cmd_options += ' -f ' + options.f
    if options.p_value_cutoff:
        cmd_options += ' --p_value_cutoff ' + options.p_value_cutoff
    if options.window_size:
        cmd_options += ' --window_size ' + options.window_size
    if options.bootstrap:
        cmd_options += ' --bootstrap ' + options.bootstrap
    if options.bootstrap_reps:
        cmd_options += ' --bootstrap_reps ' + options.bootstrap_reps

    # command with dependencies installed
    cmd = 'populations' + cmd_files + ' ' + cmd_options + ' 2>&1'
    proc = subprocess.Popen(args=cmd, shell=True)
    returncode = proc.wait()

    print '\n[INFO cmd] : ' + cmd

    # postprocesses
    try:
        shutil.copy('batch_1.populations.log', options.logfile)
    except:
        sys.stderr.write('Error in population execution; Please read the additional output (stdout)\n')
        sys.exit(1)

    try:
        shutil.move(glob.glob('*.sumstats_summary.tsv')[0], options.ss)
    except:
        print "No sumstats summary file"

    try:
        shutil.move(glob.glob('*.sumstats.tsv')[0], options.s)
    except:
        print "No sumstats file"

    # move additionnal output files
    if options.ov:
        try:
            shutil.move(glob.glob('*.vcf')[0], options.ov)
        except:
            print "No VCF files"

    if options.op:
        try:
            shutil.move(glob.glob('*.phylip')[0], options.op)
        except:
            print "No phylip file"

    if options.ol:
        try:
            shutil.move(glob.glob('*.phylip.log')[0], options.ol)
        except:
            print "No phylip.log file"

    if options.of:
        try:
            shutil.move(glob.glob('*.fa')[0], options.of)
        except:
            print "No fasta files"

    if options.os:
        try:
            shutil.move(glob.glob('*.structure.tsv')[0], options.os)
        except:
            print "No structure file"

    if options.oe:
        try:
            shutil.move(glob.glob('*.ped')[0], options.oe)
        except:
            print "No ped file"

    if options.om:
        try:
            shutil.move(glob.glob('*.map')[0], options.om)
        except:
            print "No map file"

    if options.og:
        try:
            shutil.move(glob.glob('*.genepop')[0], options.og)
        except:
            print "No genepop file"

    # copy all files inside tmp_dir into workdir or into an archive....
    list_files = glob.glob('*')

    markerszip = zipfile.ZipFile('markers.zip.temp', 'w',
                                 allowZip64=True)
    phasezip = zipfile.ZipFile('phase.zip.temp', 'w', allowZip64=True)
    unphasedzip = zipfile.ZipFile('unphased.zip.temp', 'w',
                                  allowZip64=True)
    fstzip = zipfile.ZipFile('fst.zip.temp', 'w', allowZip64=True)

    for i in list_files:
        # for each type of files

        if re.search("\.markers$", i):
            markerszip.write(os.path.basename(i))
        elif re.search("phase\.inp$", i):
            phasezip.write(os.path.basename(i))
        elif re.search("unphased\.bgl$", i):
            unphasedzip.write(os.path.basename(i))
        elif re.search('fst', i):
            fstzip.write(os.path.basename(i))
        else:

        # else return original files
            if re.search('^batch', os.path.basename(i)) \
                and not re.search("\.tsv$", os.path.basename(i)) \
                or re.search(".*_[0-9]*\.tsv$", os.path.basename(i)):
                shutil.move(i, '../galaxy_outputs')

    # close zip files
    markerszip.close()
    phasezip.close()
    unphasedzip.close()
    fstzip.close()

    # return archives
    shutil.move('fst.zip.temp', options.fst_output)
    if options.beagle and options.beagle == 'true':
        shutil.move('markers.zip.temp', options.markers_output)
        shutil.move('unphased.zip.temp', options.unphased_output)
    if options.phase and options.phase == 'true':
        shutil.move('phase.zip.temp', options.phase_output)


if __name__ == '__main__':
    __main__()


			
