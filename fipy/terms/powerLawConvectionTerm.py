#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  PyFiVol - Python-based finite volume PDE solver
 # 
 #  FILE: "powerLawConvectionTerm.py"
 #                                    created: 12/5/03 {2:50:05 PM} 
 #                                last update: 1/16/04 {11:42:44 AM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
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

import Numeric

from fivol.terms.convectionTerm import ConvectionTerm
from fivol.variables.faceVariable import FaceVariable
from fivol.tools.dimensions.physicalField import PhysicalField

class PowerLawConvectionTerm(ConvectionTerm):
    class Alpha(FaceVariable):
	def __init__(self, P):
	    FaceVariable.__init__(self, mesh = P.getMesh())
	    self.P = self.requires(P)
	    
	def calcValue(self):
	    eps = 1e-3
	    P  = self.P.getNumericValue()

            print "P: ", type(P)

	    P = Numeric.where(abs(P) < eps, eps, P)
	    
	    alpha = Numeric.where(                    P > 10.,                   (P - 1.) / P,   0.5)

	    tmp = (1. - P/10.)
	    tmpSqr = tmp * tmp
	    alpha = Numeric.where(   (10. >= P) and (P > eps), ((P-1.) + tmpSqr*tmpSqr*tmp)/P, alpha)

	    tmp = (1. + P/10.)
	    tmpSqr = tmp * tmp
	    alpha = Numeric.where((eps  >  P) and (P >= -10.),     (tmpSqr*tmpSqr*tmp - 1.)/P, alpha)
	    
	    self.value = PhysicalField(value = alpha)
