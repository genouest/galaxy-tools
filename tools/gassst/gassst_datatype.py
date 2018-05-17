import logging
import re
from galaxy.datatypes.data import *
from galaxy.datatypes.sniff import *
from galaxy.datatypes.binary import *
from galaxy.datatypes.tabular import *

log = logging.getLogger(__name__)

# Gasst datatypes
class Gassst( Tabular ):
	file_ext='gassst'

	def set_peek( self, dataset, is_multi_byte=False ):
        	if not dataset.dataset.purged:
            		dataset.peek  = "Gassst output file"
            		dataset.blurb = data.nice_size( dataset.get_size() )
        	else:
            		dataset.peek = 'file does not exist'
            		dataset.blurb = 'file purged from disk'

    	def display_peek( self, dataset ):
        	try:
            		return dataset.peek
        	except:
            		return "Gasst output file (%s)" % ( data.nice_size( dataset.get_size() ) )
