#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import tempfile
import subprocess
import glob
import shutil
import argparse
from os.path import basename
import zipfile
import tarfile
import gzip
from stacks import *


def __main__():

    # arguments recuperation

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_type')
    parser.add_argument('--input_enzyme')
    parser.add_argument('--input_single')
    parser.add_argument('--input_paired1')
    parser.add_argument('--input_paired2')
    parser.add_argument('--inputype')
    parser.add_argument('--sample_name')
    parser.add_argument('--barcode')
    parser.add_argument('--output_choice')
    parser.add_argument('--output_archive')
    parser.add_argument('--enzyme1')
    parser.add_argument('--enzyme2')
    parser.add_argument('--outype')
    parser.add_argument('--qualitenc')
    parser.add_argument('--D')
    parser.add_argument('--t', default='-1')
    parser.add_argument('--q', default='')
    parser.add_argument('--discard_file')
    parser.add_argument('--r', default='')
    parser.add_argument('--w', default='-w 0.15')
    parser.add_argument('--s', default='-s 10')
    parser.add_argument('--c', default='')
    parser.add_argument('--inline_null', default='--inline_null')
    parser.add_argument('--index_null', default='')
    parser.add_argument('--inline_inline', default='')
    parser.add_argument('--index_index', default='')
    parser.add_argument('--inline_index', default='')
    parser.add_argument('--index_inline', default='')
    parser.add_argument('--logfile')
    options = parser.parse_args()

    # create the working dir
    os.mkdir('inputs')
    os.mkdir('job_outputs')
    os.mkdir('galaxy_outputs')

    cmd_line = []
    cmd_line.append('process_radtags')
    cmd_line.extend(['-p', 'inputs'])
    cmd_line.extend(['-i', options.inputype])
    cmd_line.extend(['-b', options.barcode])

    # parse config files and create symlink into the temp dir

    if options.input_type == 'single':

        # load the config file
        input_single = options.input_single

        # parse the input_file to extract filenames and filepaths
        tab_files = galaxy_config_to_tabfiles(input_single)

        # create symlink into the temp dir
        create_symlinks_from_tabfiles(tab_files, 'inputs')
    else:

        # load config files
        input_paired1 = options.input_paired1
        input_paired2 = options.input_paired2

        # parse the input_file to extract filenames and filepaths

        tab_files_paired1 = galaxy_config_to_tabfiles(input_paired1)
        tab_files_paired2 = galaxy_config_to_tabfiles(input_paired2)

        # create symlinks into the temp dir

        create_symlinks_from_tabfiles(tab_files_paired1, 'inputs')
        create_symlinks_from_tabfiles(tab_files_paired2, 'inputs')

        cmd_line.append('-P')

    # test nb enzyme
    if options.input_enzyme == '1':
        cmd_line.extend(['-e', options.enzyme1])

    if options.input_enzyme == '2':
        cmd_line.extend(['---renz_1', options.enzyme1, '--renz_2', options.enzyme2])

    # quality
    cmd_line.extend(['-E', options.qualitenc])

    # test truncate value
    if options.t != '-1':
        cmd_line.extend(['-t', options.t])

    cmd_line.extend(['-o', 'job_outputs/'])
    cmd_line.extend(['-y', options.outype])
    cmd_line.extend([
        options.D,
        options.q,
        options.r,
        options.w,
        options.s,
        options.c,
        options.inline_null,
        options.index_null,
        options.inline_inline,
        options.index_index,
        options.inline_index,
        options.index_inline,
        ])

    print '[CMD_LINE] : ' + ' '.join(cmd_line)

    p = subprocess.call(cmd_line)

    # postprocesses

    try:
        shutil.move('job_outputs/process_radtags.log', options.logfile)
    except:
        sys.stderr.write('Error in process_radtags execution; Please read the additional output (stdout)\n')
        sys.exit(1)        

    if options.discard_file:
        discards_file_name = glob.glob('job_outputs/*.discards')[0]
        shutil.move(discards_file_name, options.discard_file)

    # manage outputs names

    change_outputs_procrad_name(os.getcwd() + '/job_outputs', options.sample_name)

    # generate additional output archive file

    if options.output_choice != '1':
        generate_additional_archive_file(os.getcwd() + '/job_outputs', options.output_archive)

    # if user has not choose the only zip archive

    if options.output_choice != '3':
        list_files = glob.glob('job_outputs/*')
        for i in list_files:
            shutil.move(i, 'galaxy_outputs')


if __name__ == '__main__':
    __main__()


