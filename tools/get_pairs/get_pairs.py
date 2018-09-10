#!/opt/python/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# --
# -- author : Pierre Pericard
# -- created : 2012-11-09
# -- modified: 2013-05-23
# --
# ----------------------------------------------------------
# --
# -- description : Get separately paired reads and singletons
# -- 				from two fastq files (left and right)
# --
# -- get_pairs.py file1.fastq file2.fastq
# --
# ----------------------------------------------------------

import argparse
import sys


if __name__ == '__main__':

    # Arguments
    parser = argparse.ArgumentParser(description='Get separately paired reads and singletons from two fastq files (left and right)')
    parser.add_argument('leftreads', metavar='leftreads', type=argparse.FileType('r'), help='left reads fastq')
    parser.add_argument('rightreads', metavar='rightreads', type=argparse.FileType('r'), help='right reads fastq')

    args = parser.parse_args()

    leftreads = args.leftreads.name
    rightreads = args.rightreads.name

    (n1, n2) = (list(), list())

    for f, n in ((leftreads, n1), (rightreads, n2)):
        with open(f, 'r') as fh:
            c = 0
            for line in fh:
                line = line.strip()
                if line:
                    c += 1
                    if c % 4 == 1:
                        n.append(line.split()[0][1:].split('/')[0])
                        if c % 40000 == 1:
                            sys.stdout.write("\r%.2f M reads read" % (c / 4000000.0))
            sys.stdout.write("\r%.2f M reads read\n" % (c / 4000000.0))

    notcommon = set(n1) ^ set(n2)

    for f in (leftreads, rightreads):

        if f == leftreads:
            basefilename = "left"
        else:
            basefilename = "right"

        pfh = open(basefilename + '.paired.fastq', 'w')
        ufh = open(basefilename + '.unpaired.fastq', 'w')
        with open(f, 'r') as fh:
            c = 0
            paired = False
            for line in fh:
                line = line.strip()
                if line:
                    c += 1
                    if c % 4 == 1:
                        paired = line.split()[0][1:].split('/')[0] not in notcommon
                        if c % 40000 == 1:
                            sys.stdout.write("\r%.2f M reads writen" % (c / 4000000.0))
                    if paired:
                        pfh.write("%s\n" % line)
                    else:
                        ufh.write("%s\n" % line)
            sys.stdout.write("\r%.2f M reads writen\n" % (c / 4000000.0))
        pfh.close()
        ufh.close()
