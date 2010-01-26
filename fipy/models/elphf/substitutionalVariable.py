#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "substitutionalVariable.py"
 #                                    created: 12/18/03 {12:18:05 AM} 
 #                                last update: 9/3/04 {10:29:54 PM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 # ###################################################################
 ##

from fipy.tools.dimensions import physicalField

from componentVariable import ComponentVariable

class SubstitutionalVariable(ComponentVariable):
    def __init__(self, mesh, parameters, solventParameters, name = '', value=0., hasOld = 1):
	self.solventParameters = solventParameters
	ComponentVariable.__init__(self, mesh = mesh, parameters = parameters, value = value, hasOld = hasOld)
## 	self.standardPotential -= physicalField.PhysicalField(self.solventParameters['standard potential'])
## 	self.barrierHeight -= physicalField.PhysicalField(self.solventParameters['barrier height'])
	
	from elphf import constant as k
	self.standardPotential -= physicalField.Scale(self.solventParameters['standard potential'],k['ENERGY'])
	self.barrierHeight -= physicalField.Scale(self.solventParameters['barrier height'], k['ENERGY'])
	if self.solventParameters.has_key('valence'):
	    self.valence -= self.solventParameters['valence']
	    
    def copy(self):
	return self.__class__(
	    mesh = self.mesh,
	    parameters = self.parameters,
	    solventParameters = self.solventParameters,
	    value = self.getValue(),
	    hasOld = 0)
	