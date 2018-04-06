#!/usr/bin/env python

"""
Create a zip archive

usage: zip.py [options]

See below for options
"""

import os
import sys
import zipfile


def __main__():

    # init
    output_zip = sys.argv[1]

    # create the zip archive
    myarchive = zipfile.ZipFile(output_zip, 'w', allowZip64=True)

    # for all files, write in the archive
    for i in range(2, len(sys.argv), 2):
        myarchive.write(sys.argv[i], os.path.basename(sys.argv[i + 1]))


if __name__ == "__main__":
    __main__()
