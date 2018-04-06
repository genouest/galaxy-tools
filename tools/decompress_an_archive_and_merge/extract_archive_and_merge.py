#!/usr/bin/env python
"""


Created by Cyril MONJEAUD
Cyril.Monjeaud@irisa.fr
Last modification: 11/19/2014

And with the help of Anthony Bretaudeau for some stuff with bz2.

"""

import bz2
import glob
import gzip
import os
import shutil
import sys
import tarfile
import zipfile

from galaxy.datatypes.checkers import check_bz2, check_gzip, check_zip


def stop_err(msg):
    sys.stderr.write('%s\n' % msg)
    sys.exit()


def main(archive, archivename, logfile, logid, workdir, merge, rm_header=0, concat=''):

    # create a temporary repository
    # tmp_dir = tempfile.mkdtemp(dir=os.getcwd())
    os.mkdir("decompress_files")

    # open log file
    mylog = open(logfile, "w")

    is_gzipped, is_gzvalid = check_gzip(archive)
    is_bzipped, is_bzvalid = check_bz2(archive)

    # extract all files in a temp directory
    # test if is a zip file
    if check_zip(archive):
        with zipfile.ZipFile(archive, 'r') as myarchive:
            myarchive.extractall("decompress_files")

    # test if is a tar file
    elif tarfile.is_tarfile(archive):
        mytarfile = tarfile.TarFile.open(archive)
        mytarfile.extractall("decompress_files")
        mytarfile.close()

    # test if is a gzip file
    elif is_gzipped and is_gzvalid:
        mygzfile = gzip.open(archive, 'rb')

        myungzippedfile = open("decompress_files/" + os.path.splitext(os.path.basename(archivename))[0], 'wb', 2**20)
        for i in iter(lambda: mygzfile.read(2**20), ''):
            myungzippedfile.write(i)

        myungzippedfile.close()
        mygzfile.close()

    elif is_bzipped and is_bzvalid:
        mybzfile = bz2.BZ2File(archive, 'rb')

        myunbzippedfile = open("decompress_files/" + os.path.splitext(os.path.basename(archivename))[0], 'wb', 2**20)
        for i in iter(lambda: mybzfile.read(2**20), ''):
                myunbzippedfile.write(i)

        myunbzippedfile.close()
        mybzfile.close()

    # test if merge is enable
    if merge == "true":
        mylog.write("Merge option is enabled with " + str(rm_header) + " lines to deleted\n\n")
        myfinalfile = open(concat, "w")
        for myfile in listdirectory("decompress_files"):
            myopenfile = open(myfile, "r")
            nblinesremove = 0
            mylog.write(os.path.basename(myfile) + " is extracted from the archive and is added into the result file\n")
            for line in myopenfile:

                # if not equal, don't write
                if int(rm_header) != nblinesremove:
                    nblinesremove = nblinesremove + 1
                else:
                    # write the line into the final file
                    myfinalfile.write(line)

        myfinalfile.close()

        shutil.rmtree("decompress_files")

    else:
        # if merge is disable
        mylog.write("Merge option is disabled\n\n")

        # move all files (recursively) in the working dir
        for myfile in listdirectory("decompress_files"):
            myfileclean = myfile.replace(" ", "\ ")

            mylog.write(os.path.basename(myfileclean) + " is extracted from the archive \n")

            fileext = os.path.splitext(myfile)[1].replace(".", "")

            # if no extension
            if fileext == '':
                shutil.move(os.path.abspath(myfile), os.path.abspath(myfile) + ".txt")

            if fileext == 'fa':
                shutil.move(os.path.abspath(myfile), os.path.abspath(myfile).replace(".fa", ".fasta"))

            if fileext == 'fq':
                shutil.move(os.path.abspath(myfile), os.path.abspath(myfile).replace(".fq", ".fastq"))

        mylog.write("\nPlease refresh your history if all files are not present\n")
        mylog.close()


# parse the directory and return files path (in a tab)
def listdirectory(path):
    myfile = []
    dirlist = glob.glob(path + '/*')
    for i in dirlist:
        # if directory
        if os.path.isdir(i):
            myfile.extend(listdirectory(i))
        # else put the file in the tab
        else:
            myfile.append(i)
    return myfile


if __name__ == "__main__":
    main(*sys.argv[1:])
