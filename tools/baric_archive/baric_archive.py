#!/usr/bin/env python
# Retrieves data from external data source applications and stores in a dataset file.
# Data source application parameters are temporarily stored in the dataset file.
import os
import socket
import sys
import urllib
from json import dumps, loads
from urllib.parse import urlparse
from urllib.request import urlopen

from galaxy.datatypes import sniff
from galaxy.datatypes.registry import Registry
from galaxy.jobs import TOOL_PROVIDED_JOB_METADATA_FILE
from galaxy.util import get_charset_from_http_headers

GALAXY_PARAM_PREFIX = 'GALAXY'
GALAXY_ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
GALAXY_DATATYPES_CONF_FILE = os.path.join(GALAXY_ROOT_DIR, 'datatypes_conf.xml')


def stop_err(msg, json_file=None):
    sys.stderr.write(msg)
    # Need to write valid (but empty) json to avoid metadata collection failure
    # leading to "unable to finish job" error with no logs
    if json_file is not None:
        json_file.write("%s\n" % dumps({}))
    sys.exit(1)


def load_input_parameters(filename, erase_file=True):
    datasource_params = {}
    try:
        json_params = loads(open(filename, 'r').read())
        datasource_params = json_params.get('param_dict')
    except Exception:
        json_params = None
        for line in open(filename, 'r'):
            try:
                line = line.strip()
                fields = line.split('\t')
                datasource_params[fields[0]] = fields[1]
            except Exception:
                continue
    if erase_file:
        open(filename, 'w').close()  # open file for writing, then close, removes params from file
    return json_params, datasource_params


def __main__():
    filename = sys.argv[1]

    user_email = sys.argv[2]
    user_id = sys.argv[3]

    try:
        max_file_size = int(sys.argv[4])
    except Exception:
        max_file_size = 0

    job_params, params = load_input_parameters(filename)
    if job_params is None:  # using an older tabular file
        enhanced_handling = False
        job_params = dict(param_dict=params)
        job_params['output_data'] = [dict(out_data_name='output',
                                          ext='auto',
                                          file_name=filename,
                                          extra_files_path=None)]
        job_params['job_config'] = dict(GALAXY_ROOT_DIR=GALAXY_ROOT_DIR, GALAXY_DATATYPES_CONF_FILE=GALAXY_DATATYPES_CONF_FILE, TOOL_PROVIDED_JOB_METADATA_FILE=TOOL_PROVIDED_JOB_METADATA_FILE)
    else:
        enhanced_handling = True
        json_file = open(job_params['job_config']['TOOL_PROVIDED_JOB_METADATA_FILE'], 'w')  # specially named file for output junk to pass onto set metadata

    datatypes_registry = Registry()
    datatypes_registry.load_datatypes(root_dir=job_params['job_config']['GALAXY_ROOT_DIR'], config=job_params['job_config']['GALAXY_DATATYPES_CONF_FILE'])

    URL = params.get('URL', None)  # using exactly URL indicates that only one dataset is being downloaded
    export = params.get('export', None)
    userkey = params.get('userkey', 'none')
    URL_method = params.get('URL_method', None)

    URL = URL + "&userkey=" + userkey + "&user_email=" + user_email + "&user_id=" + user_id

    # The Python support for fetching resources from the web is layered. urllib uses the httplib
    # library, which in turn uses the socket library.  As of Python 2.3 you can specify how long
    # a socket should wait for a response before timing out. By default the socket module has no
    # timeout and can hang. Currently, the socket timeout is not exposed at the httplib or urllib2
    # levels. However, you can set the default timeout ( in seconds ) globally for all sockets by
    # doing the following.
    socket.setdefaulttimeout(600)

    for data_dict in job_params['output_data']:
        cur_filename = data_dict.get('file_name', filename)
        cur_URL = params.get('%s|%s|URL' % (GALAXY_PARAM_PREFIX, data_dict['out_data_name']), URL)
        if not cur_URL or urlparse(cur_URL).scheme not in ('http', 'https', 'ftp'):
            open(cur_filename, 'w').write("")
            stop_err('The remote data source application has not sent back a URL parameter in the request.', json_file)

        # The following calls to urlopen() will use the above default timeout
        try:
            if not URL_method or URL_method == 'get':
                page = urlopen(cur_URL)
            elif URL_method == 'post':
                page = urlopen(cur_URL, urllib.parse.urlencode(params).encode("utf-8"))
        except Exception as e:
            stop_err('The remote data source application may be off line, please try again later. Error: %s' % str(e), json_file)
        if max_file_size:
            file_size = int(page.info().get('Content-Length', 0))
            if file_size > max_file_size:
                stop_err('The size of the data (%d bytes) you have requested exceeds the maximum allowed (%d bytes) on this server.' % (file_size, max_file_size), json_file)
        # handle files available locally
        if export:
            try:
                local_file = export + page.read()
                os.remove(cur_filename)
                os.symlink(local_file, cur_filename)
            except Exception as e:
                stop_err('Unable to symlink %s to %s:\n%s' % (local_file, cur_filename, e), json_file)
        else:
            try:
                cur_filename = sniff.stream_to_open_named_file(page, os.open(cur_filename, os.O_WRONLY | os.O_CREAT), cur_filename, source_encoding=get_charset_from_http_headers(page.headers))
            except Exception as e:
                stop_err('Unable to fetch %s:\n%s' % (cur_URL, e), json_file)

        # here import checks that upload tool performs
        if enhanced_handling:
            try:
                ext = sniff.handle_uploaded_dataset_file(filename, datatypes_registry, ext=data_dict['ext'])
            except Exception as e:
                stop_err(str(e), json_file)
            info = dict(type='dataset',
                        dataset_id=data_dict['dataset_id'],
                        ext=ext)

            json_file.write("%s\n" % dumps(info))


if __name__ == "__main__":
    __main__()
