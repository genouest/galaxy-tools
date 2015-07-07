
"""
Compressed classes
"""

import mimetypes, logging, os, os.path, sys, time, tempfile, shutil, string, glob, re, zipfile, tarfile

from galaxy.datatypes.data import Data
from galaxy.datatypes.sniff import *
from cgi import escape
from inspect import isclass
from galaxy import util
from galaxy.datatypes.metadata import MetadataElement #import directly to maintain ease of use in Datatype class definitions
from galaxy.util import inflector
from galaxy.util.bunch import Bunch
from galaxy.util.odict import odict
from galaxy.util.sanitize_html import sanitize_html
from galaxy.datatypes.checkers import *
from galaxy.datatypes import data


log = logging.getLogger(__name__)

class Zip( Data ):
    file_ext = "zip"
   
    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
	    dataset.peek = data.get_file_peek( dataset.file_name, is_multi_byte=is_multi_byte )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def sniff( self, filename ):
        if (check_zip( filename )):
            return True
        return False
	

class Tgz( Data ):
    file_ext = "tar.gz"

    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = data.get_file_peek( dataset.file_name, is_multi_byte=is_multi_byte )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def sniff( self, filename ):
        is_gzipped, is_valid = check_gzip( filename )
        is_tar = tarfile.is_tarfile( filename )
        return (is_gzipped and is_valid and is_tar)

 
class Tbz2( Data ):
    file_ext = "tar.bz2"

    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = data.get_file_peek( dataset.file_name, is_multi_byte=is_multi_byte )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def sniff( self, filename ):
        is_bzipped, is_valid = check_bz2( filename )
        is_tar = tarfile.is_tarfile( filename )
        return (is_bzipped and is_valid and is_tar)

    
class Fastqgz( Data ):
    file_ext = "fastq.gz"

    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = data.get_file_peek( dataset.file_name, is_multi_byte=is_multi_byte )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def sniff( self, filename ):
        is_gzipped, is_valid = check_gzip( filename )
        is_tar = tarfile.is_tarfile( filename )
        return (is_gzipped and is_valid and not is_tar)

class Fastqbz2( Data ):
    file_ext = "fastq.bz2"

    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = data.get_file_peek( dataset.file_name, is_multi_byte=is_multi_byte )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def sniff( self, filename ):
        is_bzipped, is_valid = check_bz2( filename )
        is_tar = tarfile.is_tarfile( filename )
        return (is_bzipped and is_valid and not is_tar)
