from galaxy import eggs

import pkg_resources
pkg_resources.require( "bx-python" )

import logging, os, sys, time, tempfile, shutil
import data
from galaxy import util
from galaxy.datatypes.sniff import *
from cgi import escape
import urllib
from bx.intervals.io import *
from galaxy.datatypes import metadata
from galaxy.datatypes.metadata import MetadataElement
from galaxy.datatypes.tabular import Tabular


class Phenotype( data.Text ):
   """Tab delimited data in Genotype format"""
   file_ext = "dqmp"

   MetadataElement( name="columns", default=3, desc="Number of columns", readonly=True )

   def __init__(self, **kwd):
       """Initialize QTLMap:Genotype datatype"""
       data.Text.__init__(self, **kwd)
      # self.do_something_else()

   def init_meta( self, dataset, copy_from=None ):
       data.Text.init_meta( self, dataset, copy_from=copy_from )

   def sniff( self, filename ):
       """
         Format du fichier de phenotype
         IDANIM FIX1 FIX2..COV1 COV2.. TRAIT1 1/0 1/0 TRAIT2 1/0 1/0 ...
       """
       handle = open(filename)
       line = handle.readline()
       handle.close()
       first = line.split()

       # 0 -> ID animal
       #read fixed effect
       i=1
       while (first[i].isalnum() and i<len(first)):
           i=i+1

       if ( i >= len(first) ):
           return False

       #read cov
       while ((i+1)<len(first) and not first[i+1].isalnum() ):
           i=i+1

       if ( i+1 >= len(first) ):
           return False

       #read trait
       while ((i+1)<len(first) and (i+2)<len(first) and not first[i].isalnum() and first[i+1].isalnum() and first[i+2].isalnum()):
           i=i+3

       if ( i != len(first) ):
           return False

       return True

class Map( Tabular ):
   """Tab delimited data in Map format"""
   file_ext = "mqmp"

   MetadataElement( name="columns", default=3, desc="Number of columns", readonly=True )

   def __init__(self, **kwd):
       """Initialize QTLMap:Map datatype"""
       data.Text.__init__(self, **kwd)
      # self.do_something_else()

   def init_meta( self, dataset, copy_from=None ):
       Tabular.init_meta( self, dataset, copy_from=copy_from )

   def sniff( self, filename ):
       """
         Format du fichier de Map
         Marker Chr D1 D2 D3 1/0
       """
       handle = open(filename)
       line = handle.readline()
       handle.close()
       first = line.split()

       if ( len(first) != 6 ):
           return False

       if ( first[5] != "1" and first[5] != "0" ):
           return False

       if ( first[2].isalnum() or first[3].isalnum() or first[4].isalnum() ):
           return False

       return True

""" Obsolete """
class Model( data.Text ):
   """Tab delimited data in Model format"""
   file_ext = "qtlmap.model"

   MetadataElement( name="columns", default=3, desc="Number of columns", readonly=True )

   def __init__(self, **kwd):
       """Initialize QTLMap:Model datatype"""
       data.Text.__init__(self, **kwd)
      # self.do_something_else()

   def init_meta( self, dataset, copy_from=None ):
       data.Text.init_meta( self, dataset, copy_from=copy_from )

   def sniff( self, filename ):
       """
         Format du fichier de Model
         nb carac
         nbfix nbcov
         car r/a/i 0/1....
       """
       handle = open(filename)
       line = handle.readline()

       #nb carac
       first = line.split()
       if ( not first[0].isdigit() ):
           return False

       ncar=int(first[0]);
       line = handle.readline()
       first = line.split()
       if ( not first[0].isdigit() ):
           return False
       if ( not first[1].isdigit() ):
           return False

       nfix=int(first[0]);
       ncov=int(first[1]);

       #nom des effets
       line = handle.readline()
       first = line.split()
       if ( len(first) < (nfix + ncov)):
              return False

       for i in range(ncar):
           line = handle.readline()
           first = line.split()
           if ( len(first) < (2+2*nfix+ncov) ):
             return False

       handle.close()

       return True

class Lrt( Tabular ):
   """Tab delimited data in Model format"""
   file_ext = "lqmp"

   MetadataElement( name="columns", default=3, desc="Number of columns", readonly=True )

   def __init__(self, **kwd):
       """Initialize QTLMap:Lrt datatype"""
       data.Text.__init__(self, **kwd)
      # self.do_something_else()

   def init_meta( self, dataset, copy_from=None ):
       Tabular.init_meta( self, dataset, copy_from=copy_from )

   def sniff( self, filename ):
       handle = open(filename)
       line = handle.readline()
       handle.close()
       first = line.split()
       if ( line.find("Chr") != -1 and line.find("Pos") != -1 and line.find("GlobalLRT") != -1):
           return True

       return False

class QtlEffect( Tabular ):
   """Tab delimited data in QTLEffect format"""
   file_ext = "eqmp"

   MetadataElement( name="columns", default=3, desc="Number of columns", readonly=True )

   def __init__(self, **kwd):
       """Initialize QTLMap:qtleffect datatype"""
       data.Text.__init__(self, **kwd)
      # self.do_something_else()

   def init_meta( self, dataset, copy_from=None ):
       Tabular.init_meta( self, dataset, copy_from=copy_from )

   def sniff( self, filename ):
       handle = open(filename)

       # to pass these lines :
       #*********************************************
       #This file is unvalide if interaction qtl case
       #*********************************************

       line = handle.readline()
       line = handle.readline()
       line = handle.readline()

       #end
       line = handle.readline()
       handle.close()
       first = line.split()

       if ( line.find("Chr") != -1 and line.find("Pos") != -1 and line.find("GlobalLRT") == -1 ):
           return True

       return False

class Pded( Tabular ):
   """Tab delimited data in Pded format"""
   file_ext = "pded"

   MetadataElement( name="columns", default=3, desc="Number of columns", readonly=True )

   def __init__(self, **kwd):
       """Initialize QTLMap:Pded datatype"""
       data.Text.__init__(self, **kwd)
      # self.do_something_else()

   def init_meta( self, dataset, copy_from=None ):
       Tabular.init_meta( self, dataset, copy_from=copy_from )

   def sniff( self, filename ):
       handle = open(filename)
       line = handle.readline()
       handle.close()
       first = line.split()
       if ( line.find("Position") != -1 and line.find("Sire") != -1 and line.find("Dam_Phase") != -1 and line.find("p(2nd") != -1):
           return True
       return False

class PdedJoin( Tabular ):
   """Tab delimited data in PdedJoin format"""
   file_ext = "pdedj"

   MetadataElement( name="columns", default=3, desc="Number of columns", readonly=True )

   def __init__(self, **kwd):
       """Initialize QTLMap:PdedJoin datatype"""
       data.Text.__init__(self, **kwd)
      # self.do_something_else()

   def init_meta( self, dataset, copy_from=None ):
       Tabular.init_meta( self, dataset, copy_from=copy_from )

   def sniff( self, filename ):
       handle = open(filename)
       line = handle.readline()
       handle.close()
       first = line.split()
       if ( line.find("Position") != -1 and line.find("Sire") != -1 and line.find("Dam_Phase") != -1 and line.find("p(Hs1/Hd1") != -1):
           return True
       return False


class Simulation( Tabular ):
   """Tab delimited data in Simulation format"""
   file_ext = "sqmp"

   MetadataElement( name="columns", default=3, desc="Number of columns", readonly=True )

   def __init__(self, **kwd):
       """Initialize QTLMap:Simulation datatype"""
       data.Text.__init__(self, **kwd)
      # self.do_something_else()

   def init_meta( self, dataset, copy_from=None ):
       Tabular.init_meta( self, dataset, copy_from=copy_from )

   def sniff( self, filename ):
       handle = open(filename)
       line = handle.readline()
       handle.close()
       first = line.split()
       if ( line.find("Trait") != -1 and line.find("LRTMAX") != -1 and line.find("Position CHR") != -1 and line.find("Position DX") != -1):
           return True
       return False


class Genotype( Tabular ):
   """Tab delimited data in Genotype format"""
   file_ext = "gqmp"
   MetadataElement( name="columns", default=3, desc="Number of columns", readonly=True )
   def __init__(self, **kwd):
       """Initialize QTLMap:Genotype datatype"""
       Tabular.__init__(self, **kwd)
      # self.do_something_else()
   def init_meta( self, dataset, copy_from=None ):
       Tabular.init_meta( self, dataset, copy_from=copy_from )
   def sniff( self, filename ):
       """
         Format du fichier de genotype
                   mark1 mark2 mark3...
         IDANIM ALL1 ALL2 ALL1 ALL2 ALL1 ALL2 ....
       """
       handle = open(filename)
       line1 = handle.readline()
       line2 = handle.readline()
       handle.close()
       header = line1.split()
       first = line2.split()

       # le nombre de marqueur definit dans l'entete doit correspondre au nombre de marqueur definit pour le premier individu
       if ( (len(header)*2)+1 != len(first) ):
          return False
       # le nombre d'allele est pair
       if ( (len(first)-1)%2 != 0 ):
          return False

       return True


class Genealogy( Tabular ):
   """Tab delimited data in Genealogy format"""
   file_ext = "pqmp"
   MetadataElement( name="columns", default=3, desc="Number of columns", readonly=True )
   def __init__(self, **kwd):
       """Initialize QTLMap:Genealogy datatype"""
       Tabular.__init__(self, **kwd)
      # self.do_something_else()
   def init_meta( self, dataset, copy_from=None ):
       Tabular.init_meta( self, dataset, copy_from=copy_from )
   def sniff( self, filename ):
       """
         Format du fichier de genealogy : ID PERE MERE GENERATION
       """
       handle = open(filename)
       line = handle.readline()
       handle.close()
       v = line.split()
       if ( len(v) != 4 ):
          return False

       if ( v[3] != "1" and v[3] != "2" and v[3] != "3" ):
          return False
       return True
