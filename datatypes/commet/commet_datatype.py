
"""
Commet input file datatype
"""


import logging, os, os.path, sys, time, tempfile, shutil, string, glob, re

from galaxy.datatypes.sniff import *
from galaxy.datatypes import data
from galaxy.datatypes.metadata import MetadataElement
from galaxy.datatypes.xml import GenericXml

log = logging.getLogger(__name__)


class Commet( data.Text ):
    """
    Resource Description Framework format (http://www.w3.org/RDF/).
    """
    file_ext = "commet"

    def sniff( self, filename ):
        """
	Returns false and the user must manually set.
        """
	with open( filename ) as handle:
	    first_line = handle.readline()
	    if first_line.startswith('//commet input file//'):
		return True

        return False

    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = data.get_file_peek( dataset.file_name, is_multi_byte=is_multi_byte )
            dataset.blurb = 'Commet input data'
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

