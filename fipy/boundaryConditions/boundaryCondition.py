#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  PFM - Python-based phase field solver
 # 
 #  FILE: "boundaryCondition.py"
 #                                    created: 11/15/03 {9:47:59 PM} 
 #                                last update: 12/8/03 {2:01:22 PM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
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
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-15 JEG 1.0 original
 # ###################################################################
 ##

"""Generic boundary condition base class
"""

import Numeric

class BoundaryCondition:
    def __init__(self,faces,value):
	"""Generic boundary condition base class.
	
	Arguments:
	    
	    'faces' -- 'list' or 'tuple' of 'Faces' to which this condition applies
	    
	    'value' -- the value to impose
	"""
        self.faces = faces
        self.value = value
	
	N = len(self.faces)
	self.faceIds = Numeric.zeros((N,))
	self.adjacentCellIds = Numeric.zeros((N,))
	for i in range(N):
	    self.faceIds[i] = self.faces[i].getId()
	    self.adjacentCellIds[i] = self.faces[i].getCellId()

    def update(self,face,cell1dia,cell1off):
	"""Return the effect of this boundary condition on the equation
	solution matrices.
    
	'update()' is called by each 'Term' of each 'Equation' for each
	'Face' that this boundary condition applies to.
	
	Arguments:
	    
	    'face' -- which 'Face' to update
	    
	    'cell1dia' -- contribution to adjacent cell diagonal by this exterior face
	    
	    'cell1off' -- contribution to b-vector by this exterior face
	
	A 'tuple' of (LL,bb) is calculated, to be added to the equation's (L,b)
	matrices at the cell bounding the specified face.
	""" 
	pass
    
    def getContribution(self,cell1dia,cell1off):
	"""Return the effect of this boundary condition on the equation
	solution matrices.
    
	'getContribution()' is called by each 'Term' of each 'Equation'.
	
	Arguments:
	    
	    'cell1dia' -- contribution to adjacent cell diagonal by this exterior face
	    
	    'cell1off' -- contribution to b-vector by this exterior face
	
	A 'tuple' of (LL,bb,ids) is calculated, to be added to the equation's (L,b)
	matrices at the cells specified by 'ids'.
	""" 
	pass
    
    def getFaces(self):
	"""Return the faces this boundary condition applies to.
	"""
        return self.faces


