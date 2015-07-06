
"""
GSV visualisation datatypes
"""


import logging, os, os.path, sys, time, tempfile, shutil, string, glob, re

from galaxy.datatypes.sniff import *
from galaxy.datatypes import data
from galaxy.datatypes.metadata import MetadataElement
from galaxy.datatypes.xml import GenericXml

log = logging.getLogger(__name__)

class GenericMapJson( data.Text ):
    """Base format class for any JSON file."""
    file_ext = "mapjson"

    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = data.get_file_peek( dataset.file_name, is_multi_byte=is_multi_byte )
            dataset.blurb = 'Mapjson data'
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def sniff( self, filename ):
        """
	Determines whether the file is JSON or not

        >>> fname = get_test_fname( 'megablast_xml_parser_test1.blastxml' )
        >>> GenericMapJson().sniff( fname )
        True
	>>> fname = get_test_fname( 'interval.interval' )
        >>> GenericMapJson().sniff( fname )
        False
	"""
	#TODO - Use a context manager on Python 2.5+ to close handle
        handle = open(filename)
        line = handle.readline()
        handle.close()


class Gjson( GenericMapJson ):
    """
    Resource Description Framework format (http://www.w3.org/RDF/).
    """
    file_ext = "gjson"

    def sniff( self, filename ):
        """
	Returns false and the user must manually set.
        """
        return False

    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = data.get_file_peek( dataset.file_name, is_multi_byte=is_multi_byte )
            dataset.blurb = 'GJSON data'
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

