
"""
Network sbml class
"""


import logging, os, os.path, sys, time, tempfile, shutil, string, glob, re

from galaxy.datatypes.sniff import *
from galaxy.datatypes import data
from galaxy.datatypes.metadata import MetadataElement
from galaxy.datatypes.xml import GenericXml
from galaxy.datatypes import data

log = logging.getLogger(__name__)

# SBML datatype
class Sbml( GenericXml ):
    file_ext = 'sbml'

    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = data.get_file_peek( dataset.file_name, is_multi_byte=is_multi_byte )
            dataset.blurb = 'SBML format'
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'



    def sniff( self, filename ):
	""""Checking for keyword - 'sbml' always in lowercase in the first few lines"""
	f = open(filename, "r")
	line1 = f.readline()
	line2 = f.readline()
	f.close()
	if re.search("<sbml.*>",line2) or re.search("<sbml.*>",line1):
	    return True
	return False


# TGDB datatype -> TinyGraphDb
class Tgdb( data.Text ):
    file_ext = 'tgdb'

    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = data.get_file_peek( dataset.file_name, is_multi_byte=is_multi_byte )
            dataset.blurb = 'TGDB format'
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'



    def sniff( self, filename ):
        """"Checking for keyword - 'Policy' and class*  always in the firsts few lines"""
        f = open(filename, "r")
        line1 = f.readline()
        line2 = f.readline()
        f.close()
        if re.search("Policy",line1) and re.search("class*",line2):
            return True

        return False


